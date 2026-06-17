import unittest
from src.sem2.lab2.threading_t5 import run_race_condition


class TestRaceCondition(unittest.TestCase):

    def test_counter_is_broken(self):
        """Тест доказывает наличие гонки данных:
        из-за потерь итераций итоговый счетчик будет строго меньше ожидаемых 300 000.
        """
        expected_value = 300_000
        actual_value = run_race_condition()

        # Проверяем, что гонка данных реально произошла
        self.assertLess(actual_value, expected_value)


if __name__ == "__main__":
    unittest.main()