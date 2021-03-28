import sudoku

s = sudoku.Sudoku(file_name='sudoku_easy1.csv')
s = s.resolve_trivial_options()
print(s)
print(s.solve())
