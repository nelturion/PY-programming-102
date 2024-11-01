import unittest
from src.lab2 import caesar as c


class CalculatorTestCase(unittest.TestCase):
    def test_encryption(self):
        self.assertEqual(c.encrypt_caesar("PYTHON"), "SBWKRQ")
        self.assertEqual(c.encrypt_caesar("python"), "sbwkrq")
        self.assertEqual(c.encrypt_caesar("Python3.12"), "Sbwkrq3.12")
        self.assertEqual(c.encrypt_caesar(""), "")
        self.assertEqual(c.encrypt_caesar("Python3.12", 7), "Wfaovu3.12")

    def test_decryption(self):
        self.assertEqual(c.decrypt_caesar("SBWKRQ"), "PYTHON")
        self.assertEqual(c.decrypt_caesar("sbwkrq"), "python")
        self.assertEqual(c.decrypt_caesar("Sbwkrq3.12"), "Python3.12")
        self.assertEqual(c.decrypt_caesar(""), "")
        self.assertEqual(c.decrypt_caesar("Wfaovu3.12", 7), "Python3.12")


if __name__ == '__main__':
    unittest.main()
