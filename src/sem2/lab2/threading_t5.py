"""
Задание 5 - пример проблемы гонки данных:

Создайте функцию, которая увеличивает глобальную переменную.
Запустите несколько потоков и покажите, как результат может быть неправильным из-за гонки данных.
"""

import threading
import sys

# Наша глобальная переменная-счетчик
counter = 0


def increment_counter(iterations: int) -> None:
    """Функция, которая многократно увеличивает глобальный счетчик."""
    global counter
    for _ in range(iterations):
        local_thread_copy = counter
        _ = hex(id(local_thread_copy))  # чтобы сломать GIL
        counter = local_thread_copy + 1


def run_race_condition() -> int:
    """Запускает три потока, которые параллельно крутят счетчик."""
    global counter
    counter = 0  # Сбрасываем перед каждым запуском, потому что мы хотим запустить гонку несколько раз

    old_interval = sys.getswitchinterval()
    sys.setswitchinterval(0.0001)  # доламываем GIL (на значениях бОльших, чем это эффект гонки незначителен)

    iterations_per_thread = 100_000

    # Создаем три потока, которые будут увеличивать одну и ту же переменную
    t1 = threading.Thread(target=increment_counter, args=(iterations_per_thread,))
    t2 = threading.Thread(target=increment_counter, args=(iterations_per_thread,))
    t3 = threading.Thread(target=increment_counter, args=(iterations_per_thread,))

    print("\n--- Старт потоков с гонкой данных ---")
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    sys.setswitchinterval(old_interval)  # чиним GIL

    # мы три (3) раза запустили потоки которые будут увеличивать счетчик
    expected = iterations_per_thread * 3
    print(f"Ожидаемый результат: {expected}")
    print(f"Фактический результат: {counter}")
    print(f"Потеряно итераций: {expected - counter}")

    return counter


if __name__ == "__main__":
    run_race_condition()
