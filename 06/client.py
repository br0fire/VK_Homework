import argparse
import socket
import threading


def send_requests(urls_file, num_threads, host, port):
    """
    Отправляет запросы на сервер и обрабатывает ответы в несколько потоков.
    """
    urls = urls_file.readlines()
    urls_per_thread = len(urls) // num_threads
    threads = []

    lock = threading.Lock()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        for i in range(num_threads):
            start_index = i * urls_per_thread
            end_index = start_index + urls_per_thread if i != num_threads - 1 else None
            urls_chunk = urls[start_index:end_index]

            thread = threading.Thread(target=send_requests_in_chunk, args=(s, urls_chunk, lock))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()


def send_requests_in_chunk(s, urls, lock):
    """
    Отправляет запросы на сервер и обрабатывает ответы для конкретного чанка URL'ов.
    """
    for url in urls:
        #lock.acquire()
        url = url.strip()
        s.sendall(url.encode())
        response = s.recv(1024).decode()
        #lock.release()
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-num_threads", type=int, default=5)
    parser.add_argument("-urls_file", type=argparse.FileType("r"), default='links.txt')
    args = parser.parse_args()
    send_requests(args.urls_file, args.num_threads, 'localhost', 8000)
