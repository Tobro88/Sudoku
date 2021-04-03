import sudoku
s = sudoku.Sudoku(file_name='sudoku_medium1.csv')
s = s.resolve_naked_singles()
print(s)
print(s.solve())
