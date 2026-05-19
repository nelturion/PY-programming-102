import sys
import time
import tracemalloc
from datetime import datetime
from functools import wraps  # Импортируем wraps


def logger(func):
    """
    Задание 1 - декоратор без собственных параметров:
    Реализовать декоратор logger, который выводит имя функции, её аргументы и время выполнения. Можно добавить вывод результата.

    >>> @logger
    ... def add(a, b):
    ...     return a + b
    >>> add(2, 3) # doctest: +ELLIPSIS
    [...] FUNCTION CALL: add
      ARGUMENTS: args=(2, 3), kwargs={}
      TIME:      ... sec
      MEMORY:    ... KiB (Peak: ... KiB)
    ----------------------------------------
    <BLANKLINE>
    5
    """

    @wraps(func)  # Сохраняет имя и docstring оригинальной функции
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

            if not should_be_silent:  # Если silent=True, то не выводим текст логов
                print(f"[{timestamp}] FUNCTION CALL: {func.__name__}")
                print(f"  ARGUMENTS: args={args}, kwargs={kwargs}")
                print(f"  TIME:      {duration:.6f} sec")
                print(f"  MEMORY:    {current / 1024:.2f} KiB (Peak: {peak / 1024:.2f} KiB)")
                print(f"{'-' * 40}\n")

    return wrapper


@logger
def loggable_function(text: str, n: int):
    """
    Функция просто выводит текст с числом
    >>> loggable_function("some text", 2, silent=True)
    'some text... 6'
    """
    return f"{text}... {n + n * n}"


# def uppercase(func):
#     def wrapper(*args, **kwargs):
#         original_result = func(*args, **kwargs)  # вызов оригинальной функции, сохраняем результат чтобы что-то там потом сделать
#         new_result = original_result.upper()  # принцип полиморфизма используется для работы с результатом функции неизвестного типа
#         return new_result
#
#     return wrapper
#
#
# @uppercase
# def loggable_function(text: str, n: int):
#     return f"{text}... {n+n*n}"

if __name__ == "__main__":
    print(loggable_function("some text", 2))
