import io
import unittest
from unittest.mock import patch
from src.sem2.lab1.decorators_t3 import logger


class TestClassLoggerDecorator(unittest.TestCase):

    def test_logging_normal_method(self):
        """1. Проверяем, что обычный метод успешно логируется и выводит имя переменной."""

        @logger(show_magic_methods=False)
        class Dummy:
            def greet(self, name):
                return f"Hello, {name}"

        # Создаем глобальную переменную для теста, чтобы её нашел наш логгер
        global test_obj
        test_obj = Dummy()

        # Перехватываем stdout (вывод принтов в консоль)
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = test_obj.greet("Alice")
            output = fake_out.getvalue()

        # Проверяем возвращаемое значение метода
        self.assertEqual(result, "Hello, Alice")

        # Проверяем, что в принтах есть нужная инфа
        self.assertIn("[LOG] OBJECT: unknown object", output)
        self.assertIn("CLASS: Dummy | METHOD: greet", output)
        self.assertIn("ARGUMENTS: args=('Alice',), kwargs={}", output)
        self.assertIn("RESULT:    Hello, Alice", output)

    def test_show_magic_methods_true(self):
        """2. Проверяем, что при show_magic_methods=True логируются магические методы."""

        @logger(show_magic_methods=True)
        class CustomValue:
            def __init__(self, val):
                self.val = val

            def __str__(self):
                return str(self.val)

        global magic_obj

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            magic_obj = CustomValue(42)  # Вызывается __init__
            str(magic_obj)  # Вызывается __str__
            output = fake_out.getvalue()

        # Проверяем, что магические методы попали в логи
        self.assertIn("METHOD: __init__", output)
        self.assertIn("METHOD: __str__", output)

    def test_show_magic_methods_false(self):
        """3. Проверяем, что при show_magic_methods=False магия игнорируется."""

        @logger(show_magic_methods=False)
        class HiddenMagic:
            def __init__(self, val):
                self.val = val

            def run(self):
                return True

        global hidden_obj

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            hidden_obj = HiddenMagic(100)  # __init__ должен проигнорироваться
            hidden_obj.run()  # run() должен залогироваться
            output = fake_out.getvalue()

        self.assertNotIn("METHOD: __init__", output)
        self.assertIn("METHOD: run", output)

    @patch('sys.argv', ['decorators_t3.py', '--silent'])
    def test_silent_mode(self):
        """4. Проверяем, что в silent-режиме логгер ничего не пишет в консоль."""

        @logger(show_magic_methods=False)
        class SilentClass:
            def do_something(self):
                return "silent"

        global silent_obj
        silent_obj = SilentClass()

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            silent_obj.do_something()
            output = fake_out.getvalue()

        # Строка вывода должна быть абсолютно пустой
        self.assertEqual(output, "")


if __name__ == '__main__':
    unittest.main()