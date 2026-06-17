import asyncio
import unittest
from contextlib import redirect_stdout
import io

# Импортируем твои асинхронные функции
# Предполагается, что код из 5 задачи лежит в файле async_tasks.py
from src.sem2.lab1.decorators_t5 import task_one, task_two, main


class TestAsyncTasks(unittest.IsolatedAsyncioTestCase):

    async def test_task_one_output(self):
        """Проверяем, что Task 1 выводит ровно 3 принта"""
        f = io.StringIO()
        # Перенаправляем стандартный вывод (print) в переменную f, чтобы перехватить текст
        with redirect_stdout(f):
            await task_one()

        output = f.getvalue().strip().split('\n')

        self.assertEqual(len(output), 3)
        self.assertIn("Task 1: Начало выполнения", output[0])
        self.assertIn("Task 1: Проснулся после 1 сек", output[1])
        self.assertIn("Task 1: Финиш после 4 сек", output[2])

    async def test_task_two_output(self):
        """Проверяем, что Task 2 выводит ровно 4 принта"""
        f = io.StringIO()
        with redirect_stdout(f):
            await task_two()

        output = f.getvalue().strip().split('\n')

        self.assertEqual(len(output), 4)
        self.assertIn("Task 2: Начало выполнения", output[0])
        self.assertIn("Task 2: Финиш", output[3])

    async def test_main_execution(self):
        """Проверяем, что общая функция main выполняется без ошибок"""
        f = io.StringIO()
        with redirect_stdout(f):
            # Запускаем main() — IsolatedAsyncioTestCase сам разберется с Event Loop
            await main()

        output = f.getvalue().strip().split('\n')
        # Всего должно быть 3 + 4 = 7 принтов
        self.assertEqual(len(output), 7)


if __name__ == "__main__":
    unittest.main()