"""Single class module with the class Sudoku.
"""

import csv

class Sudoku:
    """A class representing a Sudoku puzzle.
    """
    def __init__(self, initial = None, file_name = None):
        """Initializes a new Sudoku puzzle.

        Args:
            initial (Sudoku, optional): use to create a copy of an existing Sudoko puzzle. Defaults
            to None. If both \'initial\' and \'file_name\' are specified a ValueError is raised.
            file_name (String, optional): use to read a Sudoku puzzle from file. Defaults to None.
            If both \'initial\' and \'file_name\' are specified a ValueError is raised.

        Raises:
            ValueError: [description]
        """
        if (initial is not None) and (file_name is not None):
            raise ValueError("can not specify \'file_name\' and \'initial\'")

        if initial is None:
            self.sudoku = [[0 for x in range(9)] for y in range(9)]
            self.options = [[set([1,2,3,4,5,6,7,8,9]) for x in range(9)] for y in range(9)]
        else:
            self.sudoku = [[initial.sudoku[y][x] for x in range(9)] for y in range(9)]
            self.options = [[initial.options[y][x] for x in range(9)] for y in range(9)]

        if file_name is not None:
            self.read_sudoku_from_file(file_name)
            self.update_options()

    def __str__(self):
        return_string = ''
        for i in range(9):
            return_string += str(self.sudoku[i])
            return_string += '\n'
        return return_string

    def is_full(self):
        """checks if the Sudoku puzzle has non-zero entries in each cell

        Returns:
            boolean: True if all cells in the Sudoku puzzle have a non-zero entry
        """
        for i in range(9):
            for j in range(9):
                if self.sudoku[i][j] == 0:
                    return False
        return True

    def are_options_left(self):
        """checks if there are still valid options available for 1 or more cells in the
        Sudoku puzzle.

        Returns:
            boolean: True if there are still options available in at least 1 cell of the
            Sudoku puzzle.
        """
        for i in range(9):
            for j in range(9):
                if len(self.options[i][j]) > 0:
                    return True
        return False

    def options_left(self):
        """Returns the sum of all options still left in the puzzle.

        Returns:
            int: number of options left in the puzzle
        """
        options_total = 0
        for i in range(9):
            for j in range(9):
                options_total += len(self.options[i][j])
        return options_total

    def empty_cells_left(self):
        """Returns the number of empty cells in the puzzle.

        Returns:
            int: number of empty cells left in the puzzle
        """
        empty_cells_total = 0
        for i in range(9):
            for j in range(9):
                if self.sudoku[i][j] == 0:
                    empty_cells_total += 1
        return empty_cells_total


    def is_cell_valid(self, cell):
        """checks if the value in the cell is valid, i.e. the same value is not
        present in the same row, column or quadrant of the cell.  A zero entry is always valid.
        As a side effect of the algorithm the function also returns False if there are other
        cells in the row, column or quadrant that are invalid, even in case the cell itself is
        valid.

        Args:
            cell (2-tuple): the co-ordinates of the cell to be tested

        Returns:
            boolean: returns False if the value in the cell is invalid
        """
        if (self.sudoku[cell[0]][cell[1]]) == 0:
            return True

        # test row of the cell
        reference_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for j in range(9):
            if self.sudoku[cell[0]][j] != 0:
                if self.sudoku[cell[0]][j] not in reference_set:
                    return False
                reference_set.remove(self.sudoku[cell[0]][j])

        # test column of the cell
        reference_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for i in range(9):
            if self.sudoku[i][cell[1]] != 0:
                if self.sudoku[i][cell[1]] not in reference_set:
                    return False
                reference_set.remove(self.sudoku[i][cell[1]])

        # test quadrant of the cell
        reference_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        quadrant = (cell[0]//3, cell[1]//3) # // is the floor division operator
        for i in range(3):
            for j in range(3):
                row = quadrant[0]*3 + i
                col = quadrant[1]*3 + j
                if self.sudoku[row][col] != 0:
                    if self.sudoku[row][col] not in reference_set:
                        return False
                    reference_set.remove(self.sudoku[row][col])
        return True

    def is_sudoku_valid(self):
        """Checks if the Sudoku puzzle is valid, i.e. does not have any invalid cell entries.
        An invalid cell entry is a duplication of a value in row, column or quadrant of the
        cell.

        Returns:
            boolean: True is the Sudoku puzzle has only valid or zero-value entries.
        """
        for i in range(9):
            for j in range(9):
                if not self.is_cell_valid((i, j)):
                    return False
        return True

    def is_sudoku_solved(self):
        """Checks if the Sudoku puzzle is solved.

        Returns:
            boolean: True is the Sudoku puzzle is solved.
        """
        solved = self.is_sudoku_valid() and self.is_full()
        return solved

    def update_options(self):
        """Rewrites the options array,
        """
        if not self.is_sudoku_valid():
            raise Exception("Can not update options if puzzle is not valid.")

        # reset the options array
        self.options = [[set([1,2,3,4,5,6,7,8,9]) for x in range(9)] for y in range(9)]

        # first remove all options from cells that have non-zero value
        for cell_row in range(9):
            for cell_col in range (9):
                value = self.sudoku[cell_row][cell_col]
                if value != 0:
                    self.options[cell_row][cell_col] = set()

        # loop through all the cells in puzzle
        for cell_row in range(9):
            for cell_col in range (9):

                value = self.sudoku[cell_row][cell_col]

                #remove value from options in the row if cell is empty
                for j in range(9):
                    if self.sudoku[cell_row][j] == 0:
                        if value in self.options[cell_row][j]:
                            self.options[cell_row][j].remove(value)

                #remove value from options from column
                for i in range(9):
                    if self.sudoku[i][cell_col] == 0:
                        if value in self.options[i][cell_col]:
                            self.options[i][cell_col].remove(value)

                #remove options from box
                box = (cell_row//3, cell_col//3) # // is the floor division operator
                for i in range(3):
                    for j in range(3):
                        row = box[0]*3 + i
                        col = box[1]*3 + j
                        test = (row != cell_row) & (col != cell_col)
                        if test: # values in rows and columns have already been removed from options
                            if self.sudoku[row][col] == 0:
                                if value in self.options[row][col]:
                                    self.options[row][col].remove(value)

    def place_value(self, cell, value, inplace=True):
        """Method that places a value in a cell of the puzzle. After the value has been placed all
        options in the puzzle are updated as well. Method can be used to update the puzzle in-place
        or return a new puzzle. This different behaviour is necessary in the solve algorithm.

        Placing a zero value has no effect and is ignored.

        Args:
            cell (2-tuple of int): a tuple with row and column numer of the cell to change
            value (int): the value to be placed in the cell
            inplace (bool, optional): used to indicate if the puzzle needs be updated in-place or
            if a new puzzle with the update is returne. Defaults to True.

        Raises:
            Exception: in case an illegal value is placed an exception is thrown.

        Returns:
            Sudoku: if inplace is False a new Sudoku object is returned. Otherwise a reference to
            the original Sudoko object is returned.
        """
        if value == 0:
            return self
        if inplace:
            return_sudoku = self
        else:
            return_sudoku = Sudoku(initial=self)
        return_sudoku.sudoku[cell[0]][cell[1]] = value
        return_sudoku.options[cell[0]][cell[1]] = set()
        if not return_sudoku.is_sudoku_valid():
            print(cell, type(value))
            raise Exception ("Illegal entry into Sudoku puzzle.")
        return_sudoku.update_options()

        return return_sudoku

    def number_of_naked_singles(self):
        """Returns the number of trivial options in the Sudoku puzzle. A trivial option
        is where a cell has only a single option available.

        Returns:
            int: number of trivial options in the Sudoku
        """
        number_of_naked_singles = 0
        for i in range(9):
            for j in range(9):
                if len(self.options[i][j]) == 1:
                    number_of_naked_singles += 1
        return number_of_naked_singles

    def find_hidden_single(self):
        """Searches the puzzle for a hidden single, and returns the relevant information for the
        first find. Returns -1, -1, -1 in case no hidden single is found.

        Returns:
            int, int, int: row number, column number and value of the hidden single
        """

        for checked_value in range(1,10):
            # Check rows for a value that occurs only once in options
            for cell_row in range(9):
                counter = 0
                hidden_single_column = 0
                for cell_col in range(9):
                    if checked_value in self.options[cell_row][cell_col]:
                        counter += 1
                        hidden_single_column = cell_col
                if counter == 1:
                    return cell_row, hidden_single_column, checked_value
            # Check columns for a value that occurs once in options
            for cell_col in range(9):
                counter = 0
                hidden_single_row = 0
                for cell_row in range(9):
                    if checked_value in self. options[cell_row][cell_col]:
                        counter += 1
                        hidden_single_row = cell_row
                if counter == 1:
                    return hidden_single_row, cell_col, checked_value
            # Check boxes for a value that occurs once in options
            for box_row in range(3):
                for box_col in range(3):
                    counter = 0
                    hidden_single_row = 0
                    hidden_single_col = 0
                    for cell_rel_row in range(3):
                        for cell_rel_col in range(3):
                            cell_abs_row = box_row * 3 + cell_rel_row
                            cell_abs_col = box_col * 3 + cell_rel_col
                            if checked_value in self.options[cell_abs_row][cell_abs_col]:
                                counter += 1
                                hidden_single_row = cell_abs_row
                                hidden_single_col = cell_abs_col
                    if counter == 1:
                        return hidden_single_row, hidden_single_col, checked_value
        return -1, -1, -1

    def resolve_naked_and_hidden_singles(self):
        """Resolves all naked and hidden singles iteratively until no more naked and hidden
        singles are present in the puzzle.
        """

        finished = False

        while not finished:
            i_hidden, j_hidden, hidden_value = self.find_hidden_single()
            if i_hidden < 0:
                self.resolve_naked_singles()
                finished = True
            else:
                self.place_value((i_hidden, j_hidden), hidden_value, inplace=True)
                self.resolve_naked_singles()

    def resolve_naked_singles(self):
        """Resolves all naked singles in the Sudoku puzzle. A naked single is
        where a cell has only a single option available.

        Returns:
            Sudoku: a new Sudoku object in which all naked singles are resolved.
        """
        #curr_sudoku = Sudoku(initial=self)

        # since resolving a trivial option can create new trivial options it is necessary
        # to loop until there are no more trivial options available.

        while self.number_of_naked_singles() > 0:
            for i in range(9):
                for j in range(9):
                    if len(self.options[i][j]) == 1:
                        value = list(self.options[i][j])[0]
                        self.place_value( (i,j), value, inplace=True)

                        # if resolving a trivial option creates an invalid puzzle then there
                        # must be a programming error that did not properly create the options
                        # for each cell
                        assert self.is_sudoku_valid(), "Impossible to resolve trivial \
                            options. Resolving a trivial option resulted in an invalid Sudoku."

        return

    def print_number_of_options(self):
        """Prints the available options for each cell.
        """
        for i in range(9):
            for j in range(9):
                print(len(self.options[i][j]),end='')
            print("\n")

    def read_sudoku_from_file(self, filename):
        """Reads a Sudoku puzzle from a .csv file.

        Args:
            file (String): filename of file containing the Sudoku puzzle.

        Raises:
            Exception: in case of errors in the input file.
        """
        with open(filename, 'r') as file:
            reader = csv.reader(file, delimiter = ' ')
            row_counter = 0
            for row in reader:
                # each row is a list
                if len(row) != 9:
                    raise Exception("Too long line in the input file - wrong file syntax.")
                column_counter = 0
                for next_value in row:
                    self.place_value((row_counter, column_counter), int(next_value), inplace=True)
                    column_counter += 1
                row_counter += 1
                if row_counter > 9:
                    raise Exception("Too many rows in the input file - wrong file syntax.")

    def select_next_move(self):
        """While solving the puzzle by exploring all options, a decision is needed about which
        option to explore next. This method returns the first option value of the cell with the
        lowest number of options.

        Returns:
            int, int, int: row number, column number and value selected for the next move
        """

        i_min = 0
        j_min = 0
        minimum = 10
        for i in range(9):
            for j in range(9):
                num_of_options = len(self.options[i][j])
                if num_of_options > 0:
                    if num_of_options < minimum:
                        minimum = num_of_options
                        i_min = i
                        j_min = j
        selected_value = list(self.options[i_min][j_min])[0]
        return i_min, j_min, selected_value

    def solve(self):
        """Method to solve the Sudoku puzzle. The algorithm used is a recursive depth-first
        search algorithm with pro-active resolution of naked and hidden singles.

        Returns:
            Boolean: True if the puzzle is solved.
        """

        if self.is_sudoku_solved():
            print(self)
            return True
        else:
            if self.are_options_left():
                i_min, j_min, selected_value = self.select_next_move()
                new_puzzle = self.place_value( (i_min, j_min), selected_value, inplace=False)
                new_puzzle.resolve_naked_and_hidden_singles()
                # if new_puzzle.empty_cells_left() > 10:
                #     print(f"{new_puzzle.empty_cells_left()} {new_puzzle.options_left()}")
                if not new_puzzle.solve():
                    self.options[i_min][j_min].remove(selected_value)
                    self.resolve_naked_and_hidden_singles()
                    # if self.empty_cells_left() > 10:
                    #     print(f"{self.empty_cells_left()} {self.options_left()}")
                    if self.solve():
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                return False

    def alternative_solve(self):
        """This method is the one found in:
            https://github.com/techwithtim/Sudoku-GUI-Solver
            The method does not eliminate naked or hidden singles and therefore needs to run more
            iterations. The reduced overhead makes this method run faster on simpler puzzles but
            runs much longer (~60 times longer) on puzzles with the minimum number of hints (17)
        """

        def inner_solve(bo):
            find = inner_find_empty(bo)
            if not find:
                inner_print_board(bo)
                return True
            else:
                row, col = find
                # print(f"Tring {row}, {col}")
            for i in range(1,10):
                if inner_valid(bo, i, (row, col)):
                    bo[row][col] = i
                    if inner_solve(bo):
                        
                        return True
                    bo[row][col] = 0
            return False

        def inner_valid(bo, num, pos):

            for i in range(len(bo[0])):
                if bo[pos[0]][i] == num and pos[1] != i:
                    return False
            for i in range(len(bo)):
                if bo[i][pos[1]] == num and pos[0] != i:
                    return False
            box_x = pos[1] // 3
            box_y = pos[0] // 3
            for i in range(box_y*3, box_y*3 + 3):
                for j in range(box_x * 3, box_x*3 + 3):
                    if bo[i][j] == num and (i,j) != pos:
                        return False
            return True

        def inner_print_board(bo):

            for i in range(len(bo)):
                if i % 3 == 0 and i != 0:
                    print("- - - - - - - - - - - - - ")
                for j in range(len(bo[0])):
                    if j % 3 == 0 and j != 0:
                        print(" | ", end="")
                    if j == 8:
                        print(bo[i][j])
                    else:
                        print(str(bo[i][j]) + " ", end="")

        def inner_find_empty(bo):

            for i in range(len(bo)):
                for j in range(len(bo[0])):
                    if bo[i][j] == 0:
                        return (i, j)  # row, col
            return None

        if not inner_solve(self.sudoku):
            print("Unsolvable")
        else:
            print("Solved")
