import unittest
import time
from unittest.mock import patch
from src.sem2.lab1.decorators_t2 import retry


class TestRetryDecorator(unittest.TestCase):

    def test_successful_run(self):
        """1. Проверяем, что если функция не падает, она просто возвращает результат."""

        @retry(attempts=3, delay=0.01)
        def safe_func():
            return "success"

        self.assertEqual(safe_func(), "success")

    def test_retry_until_success(self):
        """2. Проверяем, что функция восстанавливается после нескольких падений."""
        calls = []

        @retry(attempts=3, delay=0.01, exceptions=(ValueError,))
        def unstable_func():
            calls.append(1)
            if len(calls) < 3:
                raise ValueError("Временный сбой")
            return "recovered"

        # Первые 2 раза упадет, на 3-й вернет "recovered"
        self.assertEqual(unstable_func(), "recovered")
        self.assertEqual(len(calls), 3)

    def test_raises_last_exception_when_exhausted(self):
        """3. Проверяем, что после исчерпания попыток падает последнее исключение."""

        @retry(attempts=2, delay=0.01, exceptions=(TypeError,))
        def permanently_broken():
            raise TypeError("Ошибка типов")

        with self.assertRaises(TypeError) as context:
            permanently_broken()

        # Проверяем, что прилетела именно наша ошибка с правильным текстом
        self.assertEqual(str(context.exception), "Ошибка типов")

    def test_ignores_unspecified_exceptions(self):
        """4. Проверяем, что если падает ошибка НЕ из списка, retry не пытается её повторить."""
        calls = []

        @retry(attempts=5, delay=0.01, exceptions=(ValueError,))
        def wrong_error_func():
            calls.append(1)
            raise KeyError("Эту ошибку мы не ждали. Unexpected error")

        # Должно упасть сразу же на первой попытке
        with self.assertRaises(KeyError):
            wrong_error_func()

        self.assertEqual(len(calls), 1)

    def test_delay_is_working(self):
        """5. Проверяем, что временная задержка delay действительно работает."""

        @retry(attempts=2, delay=0.1, exceptions=(ValueError,))
        def delayed_func():
            raise ValueError("Падаем")

        start_time = time.perf_counter()
        try:
            delayed_func()
        except ValueError:
            pass
        duration = time.perf_counter() - start_time

        # Должна быть как минимум одна пауза в 0.1 секунды
        self.assertGreaterEqual(duration, 0.1)


if __name__ == '__main__':
    unittest.main()
