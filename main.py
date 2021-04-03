"""SUDOKU SOLVER

Used to load a sudoku puzzle from a csv file and then solve the puzzle.


"""

import sudoku

s = sudoku.Sudoku(file_name='sudoku_17.csv')
print(s)
s.resolve_naked_singles()
print(s.solve())
