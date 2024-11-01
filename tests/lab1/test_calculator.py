import unittest
from src.lab1 import calculator


class CalculatorTestCase(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(calculator.addition(2, 2), 4.0)
        self.assertEqual(calculator.addition(2, 0), 2.0)
        self.assertEqual(calculator.addition(0, 2), 2.0)
        self.assertEqual(calculator.addition(2, -2), 0.0)
        self.assertEqual(calculator.addition(-2, -2), -4.0)

    def test_subtraction(self):
        self.assertEqual(calculator.substracition(2, 2), 0.0)
        self.assertEqual(calculator.substracition(2, 0), 2.0)
        self.assertEqual(calculator.substracition(0, 2), -2.0)
        self.assertEqual(calculator.substracition(2, -2), 4.0)
        self.assertEqual(calculator.substracition(-2, -2), 0.0)

    def test_multiplication(self):
        self.assertEqual(calculator.multiply(2, 2), 4.0)
        self.assertEqual(calculator.multiply(2, 0), 0.0)
        self.assertEqual(calculator.multiply(0, 2), 0.0)
        self.assertEqual(calculator.multiply(2, -2), -4.0)
        self.assertEqual(calculator.multiply(-2, -2), 4.0)

    def test_division(self):
        self.assertEqual(calculator.divide(2, 2), 1.0)
        self.assertEqual(calculator.divide(2, 0), "Делить на ноль можно, но только осторожно. Я не осторожный.")
        self.assertEqual(calculator.divide(0, 2), 0.0)
        self.assertEqual(calculator.divide(2, -2), -1.0)
        self.assertEqual(calculator.divide(-2, -2), 1.0)


if __name__ == '__main__':
    unittest.main()
