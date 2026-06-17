"""
Задание 6 - решение проблемы гонки данных:

Модифицируйте код из задания 5, добавив механизма блокировки threading.Lock для предотвращения гонки данных.
Покажите, что проблема действительно решилась.
"""

import threading
import sys

# Наша глобальная переменная-счетчик
counter = 0
lock = threading.Lock()


def increment_counter(iterations):
    """Безопасная версия функции, которая увеличивает глобальный счетчик"""
    global counter
    for _ in range(iterations):
        with lock:  # единственное изменение, что в этот раз мы повесим замок на доступ к переменной
            local_thread_copy = counter
            _ = hex(id(local_thread_copy))
            counter = local_thread_copy + 1


def run_safe_race_condition() -> int:
    """Запускает три потока, которые параллельно крутят счетчик."""
    global counter
    counter = 0

    old_interval = sys.getswitchinterval()
    sys.setswitchinterval(0.0001)

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
    run_safe_race_condition()
