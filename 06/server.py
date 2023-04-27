import requests
from bs4 import BeautifulSoup
import json
import re
from collections import Counter
import argparse


def get_words(url, k):
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
    top_k_words = dict(word_count.most_common(k))

    # Возвращаем результат в формате JSON
    return json.dumps(top_k_words, ensure_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', type=int, default=1)
    parser.add_argument('-k', type=int, default=1)
    args = parser.parse_args()
    url = 'https://en.wikipedia.org/wiki/Lionel_Messi'
    print(get_words(url, args.k))
