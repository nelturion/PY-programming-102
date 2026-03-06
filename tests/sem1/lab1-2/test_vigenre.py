import unittest
from src.sem1.lab1_2 import vigenre as v


class CalculatorTestCase(unittest.TestCase):
    def test_encryption(self):
        self.assertEqual(v.encrypt_vigenere("PYTHON", "A"), 'PYTHON')
        self.assertEqual(v.encrypt_vigenere("python", "a"), 'python')
        self.assertEqual(v.encrypt_vigenere("ATTACKATDAWN", "LEMON"), 'LXFOPVEFRNHR')
        self.assertEqual(v.encrypt_vigenere("AttackAtDawn", "LeMoN"), 'LxfopvEfRnhr')

    def test_decryption(self):
        self.assertEqual(v.decrypt_vigenere("PYTHON", "A"), 'PYTHON')
        self.assertEqual(v.decrypt_vigenere("python", "a"), 'python')
        self.assertEqual(v.decrypt_vigenere("LXFOPVEFRNHR", "LEMON"), 'ATTACKATDAWN')
        self.assertEqual(v.decrypt_vigenere("LxfopvEfRnhr", "LeMoN"), 'AttackAtDawn')


if __name__ == '__main__':
    unittest.main()
