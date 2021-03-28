"""Program to test reading from a Sudoku file.
"""

import sudoku

a = sudoku.Sudoku(file_name='sudoku_easy1.csv')
print(a.options[0][0])
b = a.place_value((0,0), 1)
c = sudoku.Sudoku(initial = b, file_name='blabla.csv')
print(c)
