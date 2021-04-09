"""SUDOKU SOLVER

Used to load a sudoku puzzle from a csv file and then solve the puzzle.


"""

import time
import sudoku

start_time = time.time()
s = sudoku.Sudoku(file_name='sudoku_evil1.csv')
print(s)
print(s.solve())
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
s = sudoku.Sudoku(file_name='sudoku_evil1.csv')
print(s)
s.alternative_solve()
print("--- %s seconds ---" % (time.time() - start_time))
