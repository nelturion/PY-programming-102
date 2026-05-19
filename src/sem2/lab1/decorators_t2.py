import sys
import time
from functools import wraps


def retry(attempts, delay, exceptions=None):
    """
        Задание 2 - декоратор с параметром:
        Реализовать декоратор retry(attempts, delay, exceptions=None), который повторяет вызов функции при возникновения
        ошибки из списка exceptions(любой, если список != None) attempts раз или до успеха с промежутками delay секунд.

        >>> call_count=0
        >>> @retry(attempts=3, delay=0.1, exceptions=(ValueError,))
        ... def fail_twice():
        ...     global call_count
        ...     call_count+=1
        ...     if call_count < 3:
        ...         raise ValueError("что-то не так")
        ...     return "все так"
        >>> fail_twice() # doctest: +ELLIPSIS
        [RETRY] ПОПЫТКА .../... провелена: что-то не так
        Повтор через ...с
        'все так'
    """

    if exceptions is None:
        exceptions = (Exception,)
    elif isinstance(exceptions, list):  # [нормализовать] перевести в формат тупля, чтобы except работал
        exceptions = tuple(exceptions)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Проверяем все флаги тишины, как и в логгере
            cmd_silent = "--silent" in sys.argv
            manual_silent = kwargs.pop("silent", False)
            global_silent = globals().get('silent', False)
            should_be_silent = cmd_silent or manual_silent or global_silent

            last_exception = None

            for attempt in range(attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if not should_be_silent:
                        print(f"[RETRY] ПОПЫТКА {attempt}/{attempts} провелена: {e}")

                    if attempt < attempts - 1:
                        if not should_be_silent:
                            print(f"Повтор через {delay}с")
                        time.sleep(delay)
            raise last_exception

        return wrapper

    return decorator


@retry(attempts=5, delay=.25, exceptions=(ValueError, TypeError, ZeroDivisionError,))
def unstable_calc(a: int, b: int) -> float | int:
    return a / b


if __name__ == "__main__":
    x = 1
    y = 5 * "ы"

    try:
        print(unstable_calc(x, y))
    except TypeError:
        print("таска провалена. попробуй что-то поменять, потом перезапусти программу")
