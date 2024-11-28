import unittest
from config_translator.constants import evaluate_constant_expression  # Импортируем функцию из constants

class TestParser(unittest.TestCase):
    
    # Тесты с числами
    def test_addition(self):
        self.assertEqual(evaluate_constant_expression(".{ 3 4 + }."), 7)

    def test_power(self):
        self.assertEqual(evaluate_constant_expression(".{ 2 3 pow() }."), 8)  # Пример с степенью

    def test_subtraction(self):
        self.assertEqual(evaluate_constant_expression(".{ 3 4 - }."), -1)

    # Тесты с массивами
    def test_len_string_array(self):
        self.assertEqual(evaluate_constant_expression(".{ len([ 'Fiction', 'Science', 'Biography' ]) }."), 3)  # Длина массива строк

    def test_len_numeric_array(self):
        self.assertEqual(evaluate_constant_expression(".{ len([ 1, 2, 3, 4 ]) }."), 4)  # Длина массива чисел

    def test_len_mixed_array(self):
        self.assertEqual(evaluate_constant_expression(".{ len([ 'apple', 'banana', 'cherry' ]) }."), 3)  # Длина массива строк

if __name__ == '__main__':
    unittest.main()
