import io
import os
import unittest
from contextlib import redirect_stdout
from src.sem2.lab3.filesystem_t1 import file_operations  # поправь импорт под свою структуру


class TestFileOperations(unittest.TestCase):

    def setUp(self):
        self.created_file = None

    def tearDown(self):
        # Подчищаем за собой созданный файл после теста
        if self.created_file and os.path.exists(self.created_file):
            try:
                os.chmod(self.created_file, 0o666)
                os.remove(self.created_file)
            except Exception:
                pass

    def test_file_workflow(self):
        f = io.StringIO()
        with redirect_stdout(f):
            self.created_file = file_operations()

        # Проверяем, что функция вернула путь и файл существует
        self.assertIsNotNone(self.created_file)
        self.assertTrue(os.path.exists(self.created_file))

        # Проверяем, что программа завершилась в состоянии прав 0o666
        final_mode = os.stat(self.created_file).st_mode & 0o777
        self.assertEqual(final_mode, 0o666)

        # Проверяем логи
        console_output = f.getvalue()
        self.assertIn("Успешно изменены права доступа на 0o444!", console_output)
        self.assertIn("Успешно восстановлены права доступа на 0o666!", console_output)


if __name__ == "__main__":
    unittest.main()