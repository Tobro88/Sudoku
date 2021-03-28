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
            self.__update_options()

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

    def __update_options(self):
        """Rewrites the options array
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

                #remove options from quadrant
                quadrant = (cell_row//3, cell_col//3) # // is the floor division operator
                for i in range(3):
                    for j in range(3):
                        row = quadrant[0]*3 + i
                        col = quadrant[1]*3 + j
                        test = (row != cell_row) & (col != cell_col)
                        if test: # values in rows and columns have already been removed from options
                            if self.sudoku[row][col] == 0:
                                if value in self.options[row][col]:
                                    self.options[row][col].remove(value)

    def __place_value(self, cell, value):
        """Internal method to place value. Does not return new object.

        Args:
            cell (2-tuple): cell in which value is to be placed.
            value (int): value to be placed in the cell.

        Raises:
            Exception: in case the entry into the puzzle is illegal.

        Returns:
            [type]: [description]
        """
        if value == 0:
            return

        self.sudoku[cell[0]][cell[1]] = value
        self.options[cell[0]][cell[1]] = set()

        if not self.is_sudoku_valid():
            print(cell, type(value))
            raise Exception ("Illegal entry into Sudoku puzzle.")

        self.__update_options()

    def place_value(self, cell, value):
        """Place value in a cell of the puzzle. Returns a new Sudoku instance.

        Args:
            cell (2-tuple): cell in which the value will be placed
            value (int): value to be placed in the specified cell

        Returns:
            A new Sudoku object with the entry placed.
        """
        new_sudoku = Sudoku(initial=self)
        new_sudoku.__place_value(cell, value)
        return new_sudoku

    def number_of_trivial_options(self):
        """Returns the number of trivial options in the Sudoku puzzle. A trivial option
        is where a cell has only a single option available.

        Returns:
            int: number of trivial options in the Sudoku
        """
        number_of_trivials = 0
        for i in range(9):
            for j in range(9):
                if len(self.options[i][j]) == 1:
                    number_of_trivials += 1
        return number_of_trivials

    def resolve_trivial_options(self):
        """Resolves all trivial options in the Sudoku puzzle. A trivial option is
        where a cell has only a single option available.

        Returns:
            Sudoku: a new Sudoku object in which all trivial options are resolved.
        """
        curr_sudoku = self

        # since resolving a trivial option can create new trivial options it is necessary
        # to loop until there are no more trivial options available.

        while curr_sudoku.number_of_trivial_options() > 0:
            for i in range(9):
                for j in range(9):
                    if len(curr_sudoku.options[i][j]) == 1:
                        value = list(curr_sudoku.options[i][j])[0]
                        curr_sudoku = curr_sudoku.place_value( (i,j), value)

                        # if resolving a trivial option creates an invalid puzzle then there
                        # must be a programming error that did not properly create the options
                        # for each cell
                        assert curr_sudoku.is_sudoku_valid(), "Impossible to resolve trivial \
                            options. Resolving a trivial option resulted in an invalid Sudoku."

        return curr_sudoku

    def print_number_of_options(self):
        """Prints the available options for each cell.
        """
        for i in range(9):
            for j in range(9):
                print(len(self.options[i][j]),end='')
            print("\n")

    def read_sudoku_from_file(self, file):
        """Reads a Sudoku puzzle from a .csv file.

        Args:
            file (String): filename of file containing the Sudoku puzzle.

        Raises:
            Exception: in case of errors in the input file.
        """
        with open(file, 'r') as file:
            reader = csv.reader(file, delimiter = ' ')
            row_counter = 0
            for row in reader:
                # each row is a list
                if len(row) != 9:
                    raise Exception("Too long line in the input file - wrong file syntax.")
                column_counter = 0
                for next_value in row:
                    self.__place_value( (row_counter, column_counter), int(next_value))
                    column_counter += 1
                row_counter += 1
                if row_counter > 9:
                    raise Exception("Too many rows in the input file - wrong file syntax.")

    def select_next_move(self):

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

        if self.is_sudoku_solved():
            return True
        else:
            if self.are_options_left():
                i_min, j_min, selected_value = self.select_next_move()
                new_puzzle = self.place_value( (i_min, j_min), selected_value)
                if not new_puzzle.solve():
                    self.options[i_min][j_min].remove(selected_value)
                    self.resolve_trivial_options()
                    if self.solve():
                        return True
                    else:
                        return False
                else:
                    return True                
            else:
                return False

