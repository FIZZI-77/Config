import unittest
from config_translator.constants import evaluate_constant_expression

class TestParser(unittest.TestCase):
    def test_evaluate_constant_expression(self):
        # Тесты с числами
        self.assertEqual(evaluate_constant_expression(".{ 3 4 + }."), 7)
        self.assertEqual(evaluate_constant_expression(".{ 2 3 pow() }."), 8)  # Пример с степенью
        self.assertEqual(evaluate_constant_expression(".{ 3 4 - }."), -1)


        # Тесты с массивами
        self.assertEqual(evaluate_constant_expression(".{ len([ 'Fiction', 'Science', 'Biography' ]) }."), 3)  # Длина массива
        self.assertEqual(evaluate_constant_expression(".{ len([ 1, 2, 3, 4 ]) }."), 4)  # Длина массива чисел
        self.assertEqual(evaluate_constant_expression(".{ len([ 'apple', 'banana', 'cherry' ]) }."), 3)  # Длина массива строк

if __name__ == '__main__':
    unittest.main()
