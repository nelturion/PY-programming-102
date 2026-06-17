import unittest
from src.sem2.lab1.decorators_t4 import call_limiter  # импортируй свой декоратор


class TestCallLimiter(unittest.TestCase):

    def test_limit_exceeded_raises_value_error(self):
        """Проверяем, что при превышении лимита выбрасывается ValueError"""

        @call_limiter(limit=1)
        class Dummy:

            def action(self):
                return "ok"

        obj = Dummy()
        self.assertEqual(obj.action(), "ok")

        # Второй вызов должен упасть
        with self.assertRaises(ValueError) as context:
            obj.action()

        self.assertIn(
            "Method action has exceeded its call limit of 1",
            str(context.exception),
        )

    def test_objects_isolation(self):
        """Проверяем, что у каждого объекта свои независимые счетчики"""

        @call_limiter(limit=2)
        class Dummy:

            def run(self):
                return "running"

        obj1 = Dummy()
        obj2 = Dummy()

        # Вычерпываем лимит первого объекта
        obj1.run()
        obj1.run()
        with self.assertRaises(ValueError):
            obj1.run()

        # Второй объект должен работать, у него свой лимит
        self.assertEqual(obj2.run(), "running")

    def test_methods_isolation(self):
        """Проверяем, что лимиты разных методов одного объекта не связаны"""

        @call_limiter(limit=1)
        class Dummy:

            def method_a(self):
                return "A"

            def method_b(self):
                return "B"

        obj = Dummy()

        # Блокируем метод А
        self.assertEqual(obj.method_a(), "A")
        with self.assertRaises(ValueError):
            obj.method_a()

        # Метод Б при этом обязан работать
        self.assertEqual(obj.method_b(), "B")


if __name__ == "__main__":
    unittest.main()