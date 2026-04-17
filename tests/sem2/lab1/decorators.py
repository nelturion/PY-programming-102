import unittest
from unittest.mock import patch
from io import StringIO
from src.sem2.lab1.decorators import loggable_function


class TestDecorators(unittest.TestCase):
    def test_loggable_function_output(self):
        """Тест на вывод отладочного текста logger-а."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            loggable_function("test", 1)
            output = mock_stdout.getvalue()
            self.assertIn("FUNCTION CALL: loggable_function", output)
            self.assertIn("ARGUMENTS: args=('test', 1), kwargs={}", output)
            self.assertIn("TIME:", output)
            self.assertIn("MEMORY:", output)
            self.assertIn("-" * 40, output)

    def test_loggable_function_result(self):
        """Тест на правильность возвращаемого результата."""
        with patch('sys.stdout', new_callable=StringIO):
            result = loggable_function("test", 1)
            self.assertEqual(result, "test... 2")

    def test_loggable_function_different_args(self):
        """Тест с другими аргументами."""
        with patch('sys.stdout', new_callable=StringIO):
            result = loggable_function("hello", 3)
            self.assertEqual(result, "hello... 12")  # 3 + 3*3 = 12


if __name__ == '__main__':
    unittest.main()
