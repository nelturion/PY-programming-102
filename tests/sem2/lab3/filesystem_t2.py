import os
import shutil
import unittest
import io
from contextlib import redirect_stdout

# Динамический импорт для точного определения путей src vs tests
import src.sem2.lab3.filesystem_t2 as filesystem_t2
from src.sem2.lab3.filesystem_t2 import directory_operations


class TestDirectoryOperations(unittest.TestCase):

    def setUp(self):
        # Определение директории исполняемого модуля (src/sem2/lab3)
        self.script_dir = os.path.dirname(os.path.abspath(filesystem_t2.__file__))

    def tearDown(self):
        garbage_list = [
            "nested_1",
            "t5_A",
            "extra_t4_1.txt",
            "extra_t4_2.txt",
            "extra_t4_3.txt",
            "copy_t1.txt",
            "rename_t2.txt",
            "lab3_t1_test_subject.txt"
        ]

        # Изолированная очистка каждого элемента
        for item in garbage_list:
            path = os.path.join(self.script_dir, item)
            if os.path.exists(path):
                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path, ignore_errors=True)
                    else:
                        os.chmod(path, 0o666)
                        os.remove(path)
                except Exception:
                    pass

    def test_directory_workflow(self):
        """Проверка выполнения всех этапов directory_operations."""
        f = io.StringIO()
        with redirect_stdout(f):
            base_dir = directory_operations()

        # Проверка возвращаемого пути
        self.assertEqual(base_dir, self.script_dir)

        # Проверка логов вывода (строго по тексту в вашем коде)
        console_output = f.getvalue()

        self.assertIn("1) Файл скопирован в copy_t1.txt", console_output)
        self.assertIn("3) Создали и переместили (переименовали) третий файл в nested_1", console_output)
        self.assertIn("4) Содержимое папки со скриптом", console_output)
        self.assertIn("Содержимое вложенной папки", console_output)
        self.assertIn("tree", console_output)
        self.assertIn("Папка: .", console_output)


if __name__ == "__main__":
    unittest.main()