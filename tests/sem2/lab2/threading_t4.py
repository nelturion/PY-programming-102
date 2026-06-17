import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from src.sem2.lab2.threading_t4 import print_message, run_sequential, run_threads


class TestThreads(unittest.TestCase):

    @patch('src.sem2.lab2.threading_t4.time.sleep')
    def test_print_message(self, mock_sleep):
        """Проверяем, что функция print_message вызывает sleep и печатает текст"""
        f = io.StringIO()
        with redirect_stdout(f):
            print_message("Hello", 0.5)

        mock_sleep.assert_called_once_with(0.5)
        self.assertEqual(f.getvalue().strip(), "Hello")

    @patch('src.sem2.lab2.threading_t4.time.sleep')
    def test_sequential_execution(self, mock_sleep):
        """Проверяем, что последовательный запуск вызывает sleep ровно 3 раза"""
        with redirect_stdout(io.StringIO()):
            run_sequential()
        self.assertEqual(mock_sleep.call_count, 3)

    @patch('src.sem2.lab2.threading_t4.threading.Thread')
    def test_threads_creation(self, mock_thread):
        """Проверяем, что создается и запускается ровно 3 потока"""
        # Настраиваем мок для объекта потока, чтобы start и join работали нормально
        mock_thread_instance = mock_thread.return_value

        with redirect_stdout(io.StringIO()):
            run_threads()

        # Проверяем, что Thread() был вызван 3 раза
        self.assertEqual(mock_thread.call_count, 3)
        # Проверяем, что у каждого потока был вызван метод start и join
        self.assertEqual(mock_thread_instance.start.call_count, 3)
        self.assertEqual(mock_thread_instance.join.call_count, 3)


if __name__ == "__main__":
    unittest.main()