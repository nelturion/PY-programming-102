"""
Задание 4 - работа с потоками:

Напишите функцию print_message(message, delay), которая выводит сообщение с задержкой в delay.
Запустите эту функцию 3 раза с разным текстом и одинаковой задержкой. Замерьте время.
После этого создайте 3 отдельных потока и запустите их. Также замерьте время.
"""
import threading
import time


def print_message(message: str, delay: int|float) -> None:
    """
    Вывод сообщения с задержкой
    """
    time.sleep(delay)
    print(message)

def run_sequential() -> None:
    """
    Последовательно запускаем вывод с задержкой три раза
    """
    print("начало последовательного вывода")

    start_time = time.perf_counter()

    print_message("first", 1)
    print_message("second", 1)
    print_message("third", 1)

    duration = time.perf_counter() - start_time
    print(f"Последовательно вывел за {duration:.2f} сек")

def run_threads() -> None:
    """
    Запуск трех потоков
    Доктестов не будет, потому что произошло явление гонки потоков
    (они длятся одинаковое количество времени и stdout не понимает, что закончилось раньше)
    """
    print("Старт многопоточной функции")
    start_time = time.perf_counter()

    messages = ["first", "second", "third"]
    threads = []

    for message in messages:
        t = threading.Thread(target=print_message, args=(message, 1))
        threads.append(t)
        t.start()           # не очень понятно, почему запускаем потоки тут

    for t in threads:
        t.join()

    duration = time.perf_counter() - start_time
    print(f"Функция завершила работу за {duration:.2f} сек")


if __name__ == "__main__":
    run_sequential()
    run_threads()