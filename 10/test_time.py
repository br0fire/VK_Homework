#!/usr/bin/env python

import cjson
import time
import ujson
import json
from fake_json import generate_big_json_data


def check_time(func, arr):
    start = time.time_ns()
    for x in arr:
        func(x)
    return (time.time_ns() - start) / 1_000_000


def main():
    arr_json_str = []
    arr_json_obj = []
    for i in range(1000):
        json_str, json_obj = generate_big_json_data(100)
        arr_json_str.append(json_str)
        arr_json_obj.append(json_obj)
    print(f"cjson.loads: {check_time(cjson.loads, arr_json_str)} ms")
    print(f"ujson.loads: {check_time(ujson.loads, arr_json_str)} ms")
    print(f"json.loads: {check_time(json.loads, arr_json_str)} ms")
    print(f"cjson.dumps: {check_time(cjson.dumps, arr_json_obj)} ms")
    print(f"ujson.dumps: {check_time(ujson.dumps, arr_json_obj)} ms")
    print(f"json.dumps: {check_time(json.dumps, arr_json_obj)} ms")


if __name__ == "__main__":
    main()
