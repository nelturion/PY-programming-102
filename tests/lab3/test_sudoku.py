import unittest
from src.lab3 import sudoku as s


class SudokuTestCase(unittest.TestCase):
    def test_group(self):
        # given
        values = [1, 2, 3, 4]
        values2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        n = 2
        n2 = 3
        expected_result = [[1, 2], [3, 4]]
        expected_result2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        # when
        result1 = s.group(values, n)
        result2 = s.group(values2, n2)

        # then
        self.assertListEqual(result1, expected_result)
        self.assertListEqual(result2, expected_result2)

    def test_get_row(self):
        # given
        grid_sample1 = [['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']]
        pos_sample1 = (0, 0)
        expected_res1 = ['1', '2', '.']

        grid_sample2 = [['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']]
        pos_sample2 = (1, 0)
        expected_res2 = ['4', '.', '6']

        grid_sample3 = [['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']]
        pos_sample3 = (2, 0)
        expected_res3 = ['.', '8', '9']

        grid_sample4 = [['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']]
        pos_sample4 = (0, 2)
        expected_res4 = ['1', '2', '.']

        # when
        res1 = s.get_row(grid_sample1, pos_sample1)
        res2 = s.get_row(grid_sample2, pos_sample2)
        res3 = s.get_row(grid_sample3, pos_sample3)
        res4 = s.get_row(grid_sample4, pos_sample4)

        # then
        self.assertListEqual(res1, expected_res1)
        self.assertListEqual(res2, expected_res2)
        self.assertListEqual(res3, expected_res3)
        self.assertListEqual(res4, expected_res4)

    def test_get_col(self):
        # given
        grid_sample1 = [['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']]
        pos_sample1 = (0, 0)
        expected_res1 = ['1', '4', '7']

        grid_sample2 = [['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']]
        pos_sample2 = (0, 1)
        expected_res2 = ['2', '.', '8']

        grid_sample3 = [['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']]
        pos_sample3 = (0, 2)
        expected_res3 = ['3', '6', '9']

        grid_sample4 = [['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']]
        pos_sample4 = (1, 0)
        expected_res4 = ['1', '4', '7']

        # when
        res1 = s.get_col(grid_sample1, pos_sample1)
        res2 = s.get_col(grid_sample2, pos_sample2)
        res3 = s.get_col(grid_sample3, pos_sample3)
        res4 = s.get_col(grid_sample4, pos_sample4)

        # then
        self.assertListEqual(res1, expected_res1)
        self.assertListEqual(res2, expected_res2)
        self.assertListEqual(res3, expected_res3)
        self.assertListEqual(res4, expected_res4)

    def test_get_block(self):
        # given
        grid = s.read_sudoku('../../src/lab3/puzzle1.txt')
        pos1 = (0, 1)
        pos2 = (4, 7)
        pos3 = (8, 8)
        expected_res1 = ['5', '3', '.', '6', '.', '.', '.', '9', '8']
        expected_res2 = ['.', '.', '3', '.', '.', '1', '.', '.', '6']
        expected_res3 = ['2', '8', '.', '.', '.', '5', '.', '7', '9']

        # when
        res1 = s.get_block(grid, pos1)
        res2 = s.get_block(grid, pos2)
        res3 = s.get_block(grid, pos3)

        # then
        self.assertListEqual(res1, expected_res1)
        self.assertListEqual(res2, expected_res2)
        self.assertListEqual(res3, expected_res3)

    def test_find_empty_positions(self):
        # given
        sample_grid1 = [['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']]
        sample_grid2 = [['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']]
        sample_grid3 = [['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']]
        sample_grid4 = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]

        empty_pos1 = (0, 2)
        empty_pos2 = (1, 1)
        empty_pos3 = (2, 0)
        empty_pos4 = (-1, -1)

        # when
        res1 = s.find_empty_positions(sample_grid1)
        res2 = s.find_empty_positions(sample_grid2)
        res3 = s.find_empty_positions(sample_grid3)
        res4 = s.find_empty_positions(sample_grid4)

        # then
        self.assertTupleEqual(res1, empty_pos1)
        self.assertTupleEqual(res2, empty_pos2)
        self.assertTupleEqual(res3, empty_pos3)
        self.assertEqual(res4, empty_pos4)

    def test_find_possible_values(self):
        # given
        grid = s.read_sudoku('../../src/lab3/puzzle1.txt')
        pos1 = (0, 2)
        pos2 = (4, 7)
        values_at_pos1 = {'1', '2', '4'}
        values_at_pos2 = {'2', '5', '9'}

        # when
        res1 = s.find_possible_values(grid, pos1)
        res2 = s.find_possible_values(grid, pos2)

        # then
        self.assertTrue(values_at_pos1 == res1)
        self.assertTrue(values_at_pos2 == res2)

    def test_solve(self):
        # given
        grid = [
            ["5", "3", ".", ".", "7", ".", ".", ".", "."],
            ["6", ".", ".", "1", "9", "5", ".", ".", "."],
            [".", "9", "8", ".", ".", ".", ".", "6", "."],
            ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
            ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
            ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
            [".", "6", ".", ".", ".", ".", "2", "8", "."],
            [".", ".", ".", "4", "1", "9", ".", ".", "5"],
            [".", ".", ".", ".", "8", ".", ".", "7", "9"],
        ]
        expected_solution = [['5', '3', '4', '6', '7', '8', '9', '1', '2'],
                             ['6', '7', '2', '1', '9', '5', '3', '4', '8'],
                             ['1', '9', '8', '3', '4', '2', '5', '6', '7'],
                             ['8', '5', '9', '7', '6', '1', '4', '2', '3'],
                             ['4', '2', '6', '8', '5', '3', '7', '9', '1'],
                             ['7', '1', '3', '9', '2', '4', '8', '5', '6'],
                             ['9', '6', '1', '5', '3', '7', '2', '8', '4'],
                             ['2', '8', '7', '4', '1', '9', '6', '3', '5'],
                             ['3', '4', '5', '2', '8', '6', '1', '7', '9']]

        # when
        actual_solution = s.solve(grid)

        # then
        self.assertEqual(expected_solution, actual_solution)

    def test_check_solution(self):
        # given
        solution = [['5', '3', '4', '6', '7', '8', '9', '1', '2'],
                    ['6', '7', '2', '1', '9', '5', '3', '4', '8'],
                    ['1', '9', '8', '3', '4', '2', '5', '6', '7'],
                    ['8', '5', '9', '7', '6', '1', '4', '2', '3'],
                    ['4', '2', '6', '8', '5', '3', '7', '9', '1'],
                    ['7', '1', '3', '9', '2', '4', '8', '5', '6'],
                    ['9', '6', '1', '5', '3', '7', '2', '8', '4'],
                    ['2', '8', '7', '4', '1', '9', '6', '3', '5'],
                    ['3', '4', '5', '2', '8', '6', '1', '7', '9']]

        wrong_solution = [['5', '2', '4', '6', '7', '8', '9', '1', '2'],
                          ['6', '7', '2', '1', '9', '5', '3', '4', '8'],
                          ['1', '9', '8', '3', '4', '2', '5', '6', '7'],
                          ['8', '5', '9', '7', '6', '1', '4', '2', '3'],
                          ['4', '2', '6', '8', '5', '3', '7', '9', '1'],
                          ['7', '1', '3', '9', '2', '4', '8', '5', '6'],
                          ['9', '6', '1', '5', '3', '7', '2', '8', '4'],
                          ['2', '8', '7', '4', '1', '9', '6', '3', '5'],
                          ['3', '4', '5', '2', '8', '6', '1', '7', '9']]

        solution_with_empties = [['5', '3', '.', '6', '7', '.', '.', '.', '.'],
                                 ['6', '7', '2', '1', '9', '5', '3', '4', '8'],
                                 ['1', '9', '8', '3', '4', '2', '5', '6', '7'],
                                 ['8', '5', '9', '7', '6', '1', '4', '2', '3'],
                                 ['4', '2', '6', '8', '5', '3', '7', '9', '1'],
                                 ['7', '1', '3', '9', '2', '4', '8', '5', '6'],
                                 ['9', '6', '1', '5', '3', '7', '2', '8', '4'],
                                 ['2', '8', '7', '4', '1', '9', '6', '3', '5'],
                                 ['3', '4', '5', '2', '8', '6', '1', '7', '9']]

        # when
        res = s.check_solution(solution)
        res2 = s.check_solution(wrong_solution)
        res3 = s.check_solution(solution_with_empties)

        # then
        self.assertTrue(res)
        self.assertFalse(res2)
        self.assertFalse(res3)
