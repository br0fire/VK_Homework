import argparse
import socket
import threading
from queue import Queue


def send_requests(urls_file, num_threads, host, port):
    """
    Отправляет запросы на сервер и обрабатывает ответы в несколько потоков.
    """
    urls_queue = Queue()

    threads = []

    lock = threading.Lock()


    for i in range(num_threads):
        thread = threading.Thread(target=send_requests_in_chunk, args=(host, port, urls_queue, num_threads, lock))
        threads.append(thread)
        thread.start()

    cnt = 0
    while True:
        cnt += 1
        url = urls_file.readline()
        if url:
            urls_queue.put(url)
            # print(f"{cnt} put {url}")
        else:
            for i in range(num_threads):
                urls_queue.put('end')
                # print(f"{cnt} put end")
            break

    for thread in threads:
        thread.join()
        # print("_____ends")


def send_requests_in_chunk(host, port, urls_queue, num_threads, lock):
    """
    Отправляет запросы на сервер и обрабатывает ответы для конкретного чанка URL'ов.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            # lock.acquire()
            url = urls_queue.get()
            if url == "end":
                # print("_____get end")
                # lock.release()
                break
            url = url.strip()
            s.sendall(url.encode())
            response = s.recv(1024).decode()
            if response[:5] == "error":
                with urls_queue.mutex:
                    urls_queue.queue.clear()
                for i in range(num_threads):
                    urls_queue.put('end')
                print(response)
                break
            # lock.release()
            print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-num_threads", type=int, default=5)
    parser.add_argument("-urls_file", type=argparse.FileType("r"), default='links.txt')
    args = parser.parse_args()
    send_requests(args.urls_file, args.num_threads, 'localhost', 8000)

