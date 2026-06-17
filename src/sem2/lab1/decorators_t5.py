import asyncio

import sys
import time
from functools import wraps
from datetime import datetime
import tracemalloc
import inspect


"""
    Задание 5 - введение в асинхронность:

    Реализовать две функции в асинхронном потоке. Первая должна содержать 3 принта, с asyncio.sleep(1) и asyncio.sleep(4) 
    между ними, вторая содержит 4 принта с asyncio.sleep(3), asyncio.sleep(1) и asyncio.sleep(1) между ними.
"""

def logger(func):
    # Проверяем, является ли функция асинхронной (корутиной)
    if inspect.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            cmd_silent = "--silent" in sys.argv
            manual_silent = kwargs.pop("silent", False)
            global_silent = globals().get("silent", False)
            should_be_silent = cmd_silent or manual_silent or global_silent

            tracemalloc.start()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            start = time.perf_counter()

            try:
                # ВАЖНО: здесь мы пишем await, чтобы дождаться полного выполнения асинхронной задачи!
                return await func(*args, **kwargs)
            finally:
                duration = time.perf_counter() - start
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                if not should_be_silent:
                    print(f"[{timestamp}] ASYNC FUNCTION CALL: {func.__name__}")
                    print(f"  ARGUMENTS: args={args}, kwargs={kwargs}")
                    print(f"  TOTAL TIME (with sleeps): {duration:.6f} sec")
                    print(f"  MEMORY:    {current / 1024:.2f} KiB (Peak: {peak / 1024:.2f} KiB)")
                    print(f"{'-' * 40}\n")

        return async_wrapper

    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            cmd_silent = "--silent" in sys.argv
            manual_silent = kwargs.pop("silent", False)
            global_silent = globals().get("silent", False)
            should_be_silent = cmd_silent or manual_silent or global_silent

            tracemalloc.start()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            start = time.perf_counter()

            try:
                return func(*args, **kwargs)
            finally:
                duration = time.perf_counter() - start
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                if not should_be_silent:
                    print(f"[{timestamp}] FUNCTION CALL: {func.__name__}")
                    print(f"  ARGUMENTS: args={args}, kwargs={kwargs}")
                    print(f"  TIME:      {duration:.6f} sec")
                    print(f"  MEMORY:    {current / 1024:.2f} KiB (Peak: {peak / 1024:.2f} KiB)")
                    print(f"{'-' * 40}\n")

        return wrapper

@logger
async def task_one():
    """Первая асинхронная функция с тремя принтами"""
    print("Task 1: Начало выполнения")
    await asyncio.sleep(1)
    print("Task 1: Проснулся после 1 сек")
    await asyncio.sleep(4)
    print("Task 1: Финиш после 4 сек (summary 5.0... sec)")

@logger
async def task_two():
    """Вторая асинхронная функция с четырьмя принтами"""
    print("Task 2: Начало выполнения")
    await asyncio.sleep(3)
    print("Task 2: Проснулся после 3 сек")
    await asyncio.sleep(1)
    print("Task 2: Проснулся после 1 сек")
    await asyncio.sleep(1)
    print("Task 2: Финиш после 1 сек (summary 5.0... sec)")

@logger
async def main():
    """Главная функция для одновременного запуска обеих задач.

    >>> asyncio.run(main()) # doctest: +REPORT_NDIFF
    Task 1: Начало выполнения
    Task 2: Начало выполнения
    Task 1: Проснулся после 1 сек
    Task 2: Проснулся после 3 сек
    Task 2: Проснулся после 1 сек
    Task 1: Финиш после 4 сек (summary 5.0... sec)
    Task 2: Финиш после 1 сек (summary 5.0... sec)
    """
    # asyncio.gather запускает задачи конкурентно в одном событийно-ориентированном цикле (event loop)
    await asyncio.gather(task_one(), task_two())


""" я захотел графически изобразить как это будет выглядеть :)

t1 b-c-- - -e
t2 b- --c-c-e 
t_  _ __ _ _ ___________

b - begin; c - checkpoint; e - end; "-" - 1 real second; t1 - task_one; t2 - task_two; t_ - timeline
"""

if __name__ == "__main__":
    print("=== Запуск асинхронных задач ===")
    asyncio.run(main())
