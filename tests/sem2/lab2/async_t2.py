import io
import unittest
import time
from contextlib import redirect_stdout

from src.sem2.lab2.async_t2 import main as run_parallel_tasks


class TestAsyncGather(unittest.IsolatedAsyncioTestCase):

    async def test_parallel_output_order(self):
        """Проверяем, что сообщения вывелись в порядке уменьшения задержки (1с -> 2с -> 3с)"""
        f = io.StringIO()

        with redirect_stdout(f):
            await run_parallel_tasks()

        output = f.getvalue().strip().split('\n')

        self.assertEqual(len(output), 3)
        self.assertIn("beta", output[0])  # Первым должен выйти тот, у кого 1 сек
        self.assertIn("alpha", output[1])  # Вторым — 2 сек
        self.assertIn("gamma", output[2])  # Третьим — 3 сек

    async def test_total_execution_time(self):
        """Проверяем, что задачи выполнялись КОНКУРЕНТНО (общее время около 3 сек, а не 6 сек)"""
        start = time.perf_counter()

        with redirect_stdout(io.StringIO()):
            await run_parallel_tasks()

        duration = time.perf_counter() - start

        # Если бы они шли друг за другом, было бы 2+1+3 = 6 секунд.
        # Так как они параллельны, время должно быть в районе 3 секунд (с мелким запасом на системные задержки).
        # self.assertLess(duration, 3.5)
        # self.assertGreaterEqual(duration, 3.0)
        self.assertAlmostEqual(duration, 3, delta=0.1)


if __name__ == "__main__":
    unittest.main()