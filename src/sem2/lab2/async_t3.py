"""
Задание 3 - выполнение асинхронного запроса к API:

В этом задании нужно найти несколько сайтов (лучше, чтобы время ответа у них сильно различалось).
После чего выполнить запросы к ним через библиотеку requests не используя асинхронное программирование.
Вывести порядок ответов этих сайтов, время ответа и общее время работы.
Повторить запросы, но уже используя асинхронное программирование.
"""

import asyncio
import time
import requests
import aiohttp

URLS = [
    "https://httpbin.org/delay/3",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/2",
]


def run_sync_requests():
    """
    запуск трех последовательных реквестов (так работает requests)
    """
    print("запускаем синхронные реквесты")
    start_total = time.perf_counter()

    for url in URLS:
        start_req = time.perf_counter()
        response = requests.get(url)
        duration = time.perf_counter() - start_req
        print(f"Ответ от {url} за {duration:.2f} сек ({response.status_code}).")

    total_duration = time.perf_counter() - start_total
    print(f"общее время выполнения 3 запросов: {total_duration:.2f} сек")

async def fetch_url(session, url):
    """
    Запуск одного реквеста
    """
    start_request = time.perf_counter()
    async with session.get(url) as response:
        await response.text()
        duration = time.perf_counter() - start_request
        print(f"Ответ от {url} за {duration:.2f} сек ({response.status}).")

async def run_async_requests():
    """
    запуск трех параллельных реквестов (так работает aiohttp)
    """
    print("запускаем асинхронные реквесты")
    start_total = time.perf_counter()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in URLS]
        await asyncio.gather(*tasks)

    total_duration = time.perf_counter() - start_total
    print(f"общее время выполнения 3 запросов: {total_duration:.2f} сек")


if __name__ == "__main__":
    # 1. sync requests with requests
    run_sync_requests()
    # 2. async requests with aiohttp
    asyncio.run(run_async_requests())
