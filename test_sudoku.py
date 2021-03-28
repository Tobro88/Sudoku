import sudoku
import unittest

class Test_Sudoko(unittest.TestCase):

    def test_is_full_true(self):
        puzzle = sudoku.Sudoku()
        for i in range(9):
            for j in range(9):
                puzzle.sudoku[i][j] = i+1
        self.assertEqual(puzzle.is_full(), True)

    def test_is_full_false(self):
        puzzle = sudoku.Sudoku()
        for i in range(9):
            for j in range(9):
                puzzle.sudoku[i][j] = i+1
        puzzle.sudoku[3][3] = 0
        self.assertEqual(puzzle.is_full(), False)

    def test_is_sudoku_valid_true_1(self):
        puzzle = sudoku.Sudoku(file_name='sudoku_completed_1.csv')
        self.assertTrue(puzzle.is_sudoku_valid())

    def test_is_sudoku_valid_true_2(self):
        puzzle = sudoku.Sudoku(file_name='sudoku_completed_2.csv')
        self.assertTrue(puzzle.is_sudoku_valid())

    def test_is_sudoku_valid_false_1(self):
        puzzle = sudoku.Sudoku(file_name='sudoku_completed_1.csv')
        puzzle.sudoku[3][3] = 2
        print(puzzle)
        self.assertFalse(puzzle.is_sudoku_valid())

    def test_is_sudoku_valid_false_2(self):
        puzzle = sudoku.Sudoku(file_name='sudoku_completed_1.csv')
        puzzle.sudoku[8][8] = 6
        print(puzzle)
        self.assertFalse(puzzle.is_sudoku_valid())

    


if __name__ == '__main__':
    unittest.main()
        