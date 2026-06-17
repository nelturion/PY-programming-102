import unittest
from src.sem2.lab2.threading_t6 import run_safe_race_condition


class TestSafeIncrement(unittest.TestCase):

    def test_counter_is_perfect(self):
        """Проверяем, что Lock полностью исправил гонку данных.
        потерь итераций не должно быть, а значит счетчик будет строго равен сумме изменений вносимых всеми тремя потоками
        """
        expected_value = 300_000
        actual_value = run_safe_race_condition()

        # Теперь значение должно быть строго равно ожидаемому
        self.assertEqual(actual_value, expected_value, "Lock не сработал, код всё еще ломается!")


if __name__ == "__main__":
    unittest.main()