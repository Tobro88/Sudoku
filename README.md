# Sudoku
<i>Modeling 9 x 9 Sudoku puzzles and solvers</i>

This code consists of a central module <code>sudoku.py</code> which defines a class for sudoku puzzles. The key method in the class is the <code>solve()</code> method which solves the Sudoku puzzle. The class contains a constructor method that allows Sudoku puzzles to be read from space separated csv files, of which a few are included.

## Solver algorithm

The solver algorithm is based on a back tracking algorithm and is implemented with the recursive method <code>solve()</code>.

Although the <code>solve()</code> method was not written with optimized performance in mind, it does contain two important steps that are not always found in other Sudoku solver algorithms found on Github. Inspiration was taken from Donald Knuth's description of Sudoku puzzle solving through back tracking in "The Art of Computer Programming Volume 4 Pre-fascicle 5C". By including two steps to clean up trivial cells while exploring the solution tree, gains are made through the search process compared to pure back tracking through all available options. These two steps are (1) cleaning up 'naked singles' and (2) cleaning up 'hidden singles'.

A Naked Single occurs when a cell has only one option left (all other values are already taken up in either the cell's row, column or box). A Hidden SIngle occurs when a cell contains an option that can not be found in the options of the other cells in either the cell's row, column or box.

Although these extra steps cause overhead when solving straighforward puzzles, with more complex puzzles (e.g. the <code>sudo_17.csv</code> puzzle) the perofrmance improvement is considerable.

A solver that does not use the two extra clean-up steps is also included (<code>alternative_solve()</code>) which can be used for comparing the performance of the two solver alogorithms).


