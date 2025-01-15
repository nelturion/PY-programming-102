import math
import unittest
from src.lab1_2 import rsa


class CalculatorTestCase(unittest.TestCase):
    def test_gcd(self):
        self.assertTrue(rsa.is_prime(2))
        self.assertTrue(rsa.is_prime(11))
        self.assertTrue(rsa.is_prime(17))
        self.assertFalse(rsa.is_prime(8))
        self.assertFalse(rsa.is_prime(1))
        self.assertFalse(rsa.is_prime(0))

    def test_isprime(self):
        self.assertEqual(rsa.gcd(12, 15), math.gcd(12, 15))
        self.assertEqual(rsa.gcd(3, 7), math.gcd(3, 7))

    def test_multiplicative_inverse(self):
        self.assertEqual(rsa.multiplicative_inverse(7, 40), 23)
        self.assertEqual(rsa.multiplicative_inverse(25, 72), 49)
        # кстати, в пособии от КФУ опечатка: y[0] == -23, а не -25 (стр. 24)


if __name__ == '__main__':
    unittest.main()
