import asyncio
import argparse
import json
import re
from collections import Counter
from bs4 import BeautifulSoup
import aiohttp


async def fetch_url(session, url, k):
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
        return url, top_k_words


async def run_worker(session, queue, k):
    while True:
        url = await queue.get()
        try:
            result = await fetch_url(session, url, k)
            print(f"{result[0]}: {json.dumps(result[1], ensure_ascii=False)}")
        except Exception as exc:
            print(f"Error processing URL {url}: {exc}")
        finally:
            queue.task_done()


async def fetch_all(urls_file, num_w, k):
    queue = asyncio.Queue(maxsize=num_w * 2)  # Ограничение размера очереди
    async with aiohttp.ClientSession() as session:
        workers = [
            asyncio.create_task(run_worker(session, queue, k))
            for _ in range(num_w)
        ]

        with open(urls_file) as file:
            for line in file:
                url = line.strip()
                await queue.put(url)

        await queue.join()

        for worker in workers:
            worker.cancel()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-num_workers", type=int, default=10)
    parser.add_argument("-urls_file", type=str, default='links.txt')
    args = parser.parse_args()
    asyncio.run(fetch_all(args.urls_file, args.num_workers, 3))
