"""
    Задание 1 - базовые асинхронные функции(повторение конца прошлой лабораторной работы):

    Необходимо написать асинхронную функцию, которая ждёт delay секунд и выводит message.
    Продемонстрировать, что она отрабатывает корректно (также проверить это тестами).
"""

import asyncio

async def delay_message(delay: int | float, message: str) -> None:
    """
    Асинхронная функция, которая ждет delay времени и выводит сообщение message.
    >>> asyncio.run(delay_message(1, "hello"))
    hello
    """
    await asyncio.sleep(delay)
    print(message)


if __name__ == '__main__':
    asyncio.run(delay_message(1.5, "ого, прошло полторы секунды"))