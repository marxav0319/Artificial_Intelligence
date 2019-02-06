import os
import unittest

from hill_climbing import hill_climbing
from iterative_deepening import iterative_deepening

TEST_INPUTS = [
                'test_inputs/1.txt',
                'test_inputs/2.txt',
                'test_inputs/3.txt',
                'test_inputs/4.txt',
                'test_inputs/5.txt',
                'test_inputs/6.txt',
                'test_inputs/7.txt',
              ]

SOLUTIONS = [
                '2 0 1 2',
                'No solution',
                'No solution',
                '1 2 3 3 1 3 2',
                '3 0 0 3 3 1 2',
                '0 0 1 2 3 0 0',
                '3 0 1 1 0 0 2 3'
            ]

class Test_Search_Algorithms(unittest.TestCase):

    def test_iterative_deepening_1(self):
        self.assertEqual(iterative_deepening(TEST_INPUTS[0]), SOLUTIONS[0])

    def test_iterative_deepening_2(self):
        self.assertEqual(iterative_deepening(TEST_INPUTS[1]), SOLUTIONS[1])

    def test_iterative_deepening_3(self):
        self.assertEqual(iterative_deepening(TEST_INPUTS[2]), SOLUTIONS[2])

    def test_iterative_deepening_4(self):
        self.assertEqual(iterative_deepening(TEST_INPUTS[3]), SOLUTIONS[3])

    def test_iterative_deepening_5(self):
        self.assertEqual(iterative_deepening(TEST_INPUTS[4]), SOLUTIONS[4])

    def test_iterative_deepening_6(self):
        self.assertEqual(iterative_deepening(TEST_INPUTS[5]), SOLUTIONS[5])

    def test_iterative_deepening_7(self):
        self.assertEqual(iterative_deepening(TEST_INPUTS[6]), SOLUTIONS[6])

    def test_hill_climbing_1(self):
        self.assertEqual(hill_climbing(TEST_INPUTS[0]), SOLUTIONS[0])

    def test_hill_climbing_2(self):
        self.assertEqual(hill_climbing(TEST_INPUTS[1]), SOLUTIONS[1])

    def test_hill_climbing_3(self):
        self.assertEqual(hill_climbing(TEST_INPUTS[2]), SOLUTIONS[2])

    def test_hill_climbing_4(self):
        self.assertEqual(hill_climbing(TEST_INPUTS[3]), SOLUTIONS[3])

    def test_hill_climbing_5(self):
        self.assertEqual(hill_climbing(TEST_INPUTS[4]), SOLUTIONS[4])

    def test_hill_climbing_6(self):
        self.assertEqual(hill_climbing(TEST_INPUTS[5]), SOLUTIONS[5])

    def test_hill_climbing_7(self):
        self.assertEqual(hill_climbing(TEST_INPUTS[6]), SOLUTIONS[6])

if __name__ == '__main__':
    unittest.main()
