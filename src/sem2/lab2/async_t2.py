import asyncio
from src.sem2.lab2.async_t1 import delay_message


async def main():
    """
        Задание 2 - асинхронное выполнение нескольких задач с asyncio.gather:

        Используя предыдущую функцию, сделать три одновременных вызова функции с delay равными 2, 1 и 3 и различными message. Вывести сообщения
    >>> asyncio.run(main())
    beta
    alpha
    gamma
    """
    await asyncio.gather(
        delay_message(2, "alpha"),
        delay_message(1, "beta"),
        delay_message(3, "gamma")
    )


if __name__ == '__main__':
    asyncio.run(main())
