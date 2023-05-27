import requests
from bs4 import BeautifulSoup
import json
import re
from collections import Counter
import argparse
import socket
import threading
from queue import Queue


class Worker(threading.Thread):
    def __init__(self, id, task_queue, stats, stats_lock, k):
        threading.Thread.__init__(self)
        self.id = id
        self.task_queue = task_queue
        self.stats = stats
        self.stats_lock = stats_lock
        self.k = k

    def run(self):
        while True:
            # получаем задачу из очереди
            conn, url = self.task_queue.get()
            try:
                # обрабатываем url и отправляем результат клиенту
                result = self.get_words(url)
                response = f"{url}: {result}".encode("utf-8")
                conn.sendall(response)
            except Exception as e:
                print(f"Error processing URL {url}: {e}")
                conn.sendall(f"{url}: error".encode("utf-8"))
            finally:
                # сообщаем, что задача выполнена
                self.task_queue.task_done()

            # увеличиваем статистику
            with self.stats_lock:
                self.stats['total_processed'] += 1
                print(f"Worker {self.id} processed {url}")
                print(f"Total processed: {self.stats['total_processed']}")

    def get_words(self, url):
        # Отправляем GET-запрос по указанному URL
        response = requests.get(url)
        # Парсим HTML-код и получаем текст
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        
        # Удаляем спецсимволы, знаки пунктуации и приводим к нижнему регистру
        text = re.sub('[^A-Za-zА-Яа-я0-9]+', ' ', text)
        text = text.lower()

        # Разбиваем текст на слова и считаем количество вхождений каждого слова
        words = text.split()
        word_count = Counter(words)

        # Получаем топ k наиболее часто встречающихся слов
        top_k_words = dict(word_count.most_common(self.k))

        # Возвращаем результат в формате JSON
        return json.dumps(top_k_words, ensure_ascii=False)


class MasterServer:
    def __init__(self, host, port, workers, k):
        self.host = host
        self.port = port
        self.k = k
        self.workers = workers
        self.task_queue = Queue()
        self.stats_lock = threading.Lock()
        self.stats = {
            'total_processed': 0
        }

    def run(self):
        # запускаем мастер-сервер на прослушивание запросов
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()

            print(f"Master server started at {self.host}:{self.port} with {self.workers} workers")

            # создаем воркеров и запускаем их
            for i in range(self.workers):
                worker = Worker(i + 1, self.task_queue, self.stats, self.stats_lock, self.k)
                worker.start()

            # принимаем запросы от клиентов
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        url = data.decode("utf-8").strip()
                        # print(f"Received URL: {url}")
                        self.task_queue.put((conn, url))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', type=int, default=5)
    parser.add_argument('-k', type=int, default=3)
    args = parser.parse_args()

    server = MasterServer('localhost', 8000, args.w, args.k)
    server.run()
