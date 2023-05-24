import json
from faker import Faker
import random


def generate_big_json_data(n):
    fake = Faker()
    data = {}
    for _ in range(n):
        key = fake.word()
        if random.choice([True, False]):
            value = fake.random_int(min=1, max=n)
        else:
            value = fake.word()
        data[key] = value

    return json.dumps(data), data
