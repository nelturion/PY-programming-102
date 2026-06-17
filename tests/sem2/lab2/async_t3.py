import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import AsyncMock, MagicMock, patch

# Абсолютный импорт с учетом твоей структуры папок
from src.sem2.lab2.async_t3 import run_async_requests, run_sync_requests


class TestApiRequestsMocked(unittest.IsolatedAsyncioTestCase):

    @patch('src.sem2.lab2.async_t3.requests.get')
    def test_sync_execution_flow(self, mock_get):
        """Тестируем синхронный запуск: проверяем, что вызывается 3 раза"""
        # Настраиваем фейковый ответ от сервера
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        f = io.StringIO()
        with redirect_stdout(f):
            total_time = run_sync_requests()

        # Проверяем, что requests.get дёрнули ровно 3 раза (по разу на каждый URL)
        self.assertEqual(mock_get.call_count, 3)
        self.assertIsNone(total_time)

    @patch('src.sem2.lab2.async_t3.aiohttp.ClientSession.get')
    async def test_async_execution_flow(self, mock_get):
        """Тестируем асинхронный запуск с подменой контекстного менеджера aiohttp"""
        # Создаем фейковый объект ответа aiohttp
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value="{}")

        # Магия для мока асинхронного `async with session.get(...)`
        mock_get.return_value.__aenter__.return_value = mock_response

        f = io.StringIO()
        with redirect_stdout(f):
            total_time = await run_async_requests()

        # Проверяем, что кэширование и сборка задач сработали (3 вызова)
        self.assertEqual(mock_get.call_count, 3)
        self.assertIsNone(total_time)


if __name__ == "__main__":
    unittest.main()