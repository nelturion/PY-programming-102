import asyncio
import io
import unittest
from contextlib import redirect_stdout

from src.sem2.lab2.async_t1 import delay_message


class TestDelayMessage(unittest.IsolatedAsyncioTestCase):

    async def test_delay_message_output(self):
        """Проверяем, что функция выводит ровно то сообщение, которое мы передали"""
        f = io.StringIO()
        test_msg = "Test Async Message"

        with redirect_stdout(f):
            await delay_message(0.1, test_msg)

        self.assertEqual(f.getvalue().strip(), test_msg)

    async def test_execution_time(self):
        """Проверяем, что функция реально спала не меньше delay"""
        start_time = asyncio.get_event_loop().time()
        delay = 0.5

        with redirect_stdout(io.StringIO()):
            await delay_message(delay, "...")

        end_time = asyncio.get_event_loop().time()
        duration = end_time - start_time

        # Время выполнения должно быть больше или равно задержки
        self.assertGreaterEqual(duration, delay)


if __name__ == "__main__":
    unittest.main()