import unittest
from unittest.mock import patch
import io
from contextlib import redirect_stdout
import os

# Импортируем модули
from src.sem2.lab3.filesystem_t3 import system_manager


class TestSystemManager(unittest.TestCase):

    @patch('builtins.input')
    def test_menu_flow_info_and_exit(self, mock_input):
        """Проверка сценария: просмотр инфо о системе (f) и выход (g)."""
        # Имитируем ввод пользователя последовательно: сначала 'f', затем 'g'
        mock_input.side_effect = ['f', 'g']

        f = io.StringIO()
        with redirect_stdout(f):
            system_manager()

        console_output = f.getvalue()

        # Проверяем, что меню вывелось и отработали нужные функции
        self.assertIn("ИНТЕРАКТИВНОЕ МЕНЮ УПРАВЛЕНИЯ СИСТЕМОЙ", console_output)
        self.assertIn("ИНФОРМАЦИЯ О СИСТЕМЕ:", console_output)
        self.assertIn("Завершение работы скрипта.", console_output)

    @patch('builtins.input')
    def test_env_variables_addition(self, mock_input):
        """Проверка работы с переменными окружения (добавление переменной)."""
        # Выбираем 'd' (окружение), затем '2' (добавить), вводим ключ, значение, затем 'g' (выход)
        mock_input.side_effect = ['d', '2', 'TEST_LAB_KEY', 'LabValue123', 'g']

        f = io.StringIO()
        with redirect_stdout(f):
            system_manager()

        # Проверяем, что переменная действительно физически появилась в окружении процесса
        self.assertEqual(os.environ.get('TEST_LAB_KEY'), 'LabValue123')

        # Подчищаем тестовую переменную за собой
        if 'TEST_LAB_KEY' in os.environ:
            del os.environ['TEST_LAB_KEY']


if __name__ == "__main__":
    unittest.main()