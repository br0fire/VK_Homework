import asyncio
import argparse
import json
import re
from collections import Counter
from bs4 import BeautifulSoup
import aiohttp


async def fetch_url(url, k):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=5) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text()

            text = re.sub('[^A-Za-zА-Яа-я0-9]+', ' ', text)
            text = text.lower()

            words = text.split()
            word_count = Counter(words)

            # Получаем топ k наиболее часто встречающихся слов
            top_k_words = dict(word_count.most_common(k))

            # Возвращаем результат в формате JSON
            return json.dumps(top_k_words, ensure_ascii=False)


async def run_worker(queue, k):
    while True:
        url = await queue.get()
        try:
            result = await fetch_url(url, k)
            print(f"{url}: {result}")
        except Exception as exc:
            print(f"Error processing URL {url}: {exc}")
        finally:
            queue.task_done()


async def fetch_batch(urls, num_w, k):
    queue = asyncio.Queue()
    workers = [
        asyncio.create_task(run_worker(queue, k))
        for _ in range(num_w)
    ]

    for url in urls:
        await queue.put(url)

    await queue.join()

    for worker in workers:
        worker.cancel()


async def fetch_all(urls_file, num_w, k):
    urls = urls_file.readlines()
    urls_per_thread = len(urls) // num_w
    arr = []
    for i in range(num_w):
        start_index = i * urls_per_thread
        end_index = start_index + urls_per_thread if i != num_w - 1 else None
        urls_chunk = urls[start_index:end_index]

        arr.append(asyncio.create_task(fetch_batch(urls_chunk, num_w, k)))

    await asyncio.gather(*arr, return_exceptions=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("num_workers", type=int, default=5)
    parser.add_argument("urls_file", type=argparse.FileType("r"),
                        default='links.txt')
    args = parser.parse_args()
    asyncio.run(fetch_all(args.urls_file, args.num_workers, 3))
