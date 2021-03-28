import sys

class SudokuSolver:

    def select_next_move(self, puzzle):

        i_min = 0
        j_min = 0
        minimum = 10
        for i in range(9):
            for j in range(9):
                num_of_options = len(puzzle.options[i][j])
                if num_of_options > 0:
                    if num_of_options < minimum:
                        minimum = num_of_options
                        i_min = i
                        j_min = j
        selected_value = list(puzzle.options[i_min][j_min])[0]
        return i_min, j_min, selected_value



    def solve(self, puzzle):

        # is the Sudoku solved (sudoku is valid and there are no more empty cells)?
        # If yes, print sudoku and end.
        # Else if there are no more options left then return "Fail"
        # (I) find first option of cell with least options
        # apply the option
        # solve
        # if "Fail" then remove option from the list, go back to (I)

        if puzzle.is_sudoku_solved():
            print("Hoera!")
            print(puzzle)
            sys.exit()

        if not puzzle.are_options_left():
            print("No more options left in puzzle.")
            return

        while True:

            i_min, j_min, selected_value = self.select_next_move(puzzle)
            print(i_min, j_min, selected_value)

            target_sudoku = puzzle.place_value( (i_min, j_min), selected_value)
            target_sudoku = target_sudoku.resolve_trivial_options()
            self.solve(target_sudoku)
            # if we reached here, then the option didn't work
            puzzle.options[i_min][j_min].remove(selected_value)
            puzzle = puzzle.resolve_trivial_options()

            if puzzle.is_sudoku_solved():
                print("Hoera!")
                print(puzzle)
                sys.exit()

            return
