from itertools import product
import time

# solve method doesn't check for multiple solutions


class SudokuGrid:
    def __init__(self, array=None):
        self.array = array
        if array is None:
            self.array = [[0 for _ in range(9)] for _ in range(9)]
        self.initial_values = self.set_initial_values()
        self.solved = False
        self.possibilities = self.init_possibles()
        self.changes = True

    def set_row_col(self, row, col, x):
        """sets the value of the cell at row,col to x"""
        try:
            self.array[row][col] = int(x)
        except:
            print(f"Didn't input an integer {x} {type(x)}")

    def get_row_col(self, row, col):
        """gets the value of the cell at row,col"""
        return self.array[row][col]

    def set_initial_values(self):
        """stores the initial values in the form of a dictionary with entries "row col":value"""
        initial_values = {}
        for row in range(9):
            for col in range(9):
                if self.get_row_col(row, col) != 0:
                    initial_values[f"{row} {col}"] = self.get_row_col(row, col)
        return initial_values

    def is_valid(self):
        """Checks if the sudoku has any errors"""
        for row in range(9):
            for col in range(9):
                if not self.is_possible(row, col):
                    return False
        return True

    def is_possible(self, row, col, value=None):
        """
        Checks if a given position i, j sees the same value in either the same
        row, column, or box of the sudoku grid
        Returns False if the number is INVALID
        Returns True if the number is VALID
        """
        if value is None:
            value = self.get_row_col(row, col)
        row_other = [self.array[row][k] for k in range(9) if k != col]
        col_other = [self.array[k][col] for k in range(9) if k != row]
        box = [self.array[ind[0]][ind[1]] for ind in self.get_box(row, col)]
        checks = row_other + col_other + box
        for num in checks:
            if num == value:
                return False
        return True

    def get_box(self, i, j):
        """
        returns the indices of the * other * cells in the box
        DOES NOT include[i, j] in the list
        """
        # round down both indices to nearest multiple of 3
        i_, j_ = i//3*3, j//3*3
        indices = [[a, b] for a, b in product(
            range(i_, i_+3), range(j_, j_+3)) if [a, b] != [i, j]]
        return indices

    def display(self):
        """prints the sudokugrid to the console"""
        for row in self.array:
            for num in row:
                print(num, end=' ')
            print()
        print("\n")

    def init_possibles(self):
        """creates a dictionary consisting of possible values for each cell"""
        possibilities = [[{} for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                if f"{row} {col}" in self.initial_values:
                    continue
                else:
                    for x in range(1, 10):
                        if self.is_possible(row, col, x):
                            possibilities[row][col][f"{x}"] = x
        return possibilities

    def update_possibles(self):
        """Updates possible candidates in each cell
        Note only removes candidates as that is what is required"""
        for row in range(9):
            for col in range(9):
                if self.get_row_col(row, col) != 0:
                    self.possibilities[row][col] = {}
                else:
                    to_remove = []
                    for key in self.possibilities[row][col].keys():
                        if not self.is_possible(row, col, int(key)):
                            to_remove += key
                    if to_remove:
                        for key in to_remove:
                            self.possibilities[row][col].pop(key)

    def find_naked_singles(self):
        """finds cells which have only one candidate number and fills them"""
        for row in range(9):
            for col in range(9):
                if len(self.possibilities[row][col]) == 1:
                    x = list(self.possibilities[row][col].values())[0]
                    self.set_row_col(row, col, x)
                    self.changes += [[row, col, x]]

    def find_single_row(self):
        """for each row finds if any numbers can only be placed in one cell and places them there"""
        for row in range(9):
            for x in range(1, 10):
                value = str(x)
                value_count = 0
                value_row_cols = []
                for col in range(9):
                    if value in self.possibilities[row][col]:
                        value_count += 1
                        value_row_cols.append([row, col])
                if value_count == 1:
                    row, col = value_row_cols[0]
                    self.set_row_col(row, col, x)
                    self.changes += [[row, col, x]]

    def find_single_col(self):
        """for each column finds if any numbers can only be placed in one cell and places them there"""
        for col in range(9):
            for x in range(1, 10):
                value = str(x)
                value_count = 0
                value_row_cols = []
                for row in range(9):
                    if value in self.possibilities[row][col]:
                        value_count += 1
                        value_row_cols.append([row, col])
                if value_count == 1:
                    row, col = value_row_cols[0]
                    self.set_row_col(row, col, x)
                    self.changes += [[row, col, x]]

    def find_single_box(self):
        """for each box checks if any numbers can only be placed in one cell and then places them there"""
        for index in range(9):
            i, j = index // 3 * 3, index % 3 * 3
            box = [[i, j]] + self.get_box(i, j)
            for x in range(1, 10):
                value = str(x)
                value_count = 0
                value_row_cols = []
                for pair in box:
                    if value in self.possibilities[pair[0]][pair[1]]:
                        value_count += 1
                        value_row_cols.append([pair[0], pair[1]])
                if value_count == 1:
                    row, col = value_row_cols[0]
                    self.set_row_col(row, col, x)
                    self.changes += [[row, col, x]]

    def find_hidden_singles(self):
        """Performs all above searches"""
        self.changes = []
        self.find_naked_singles()
        self.find_single_row()
        self.find_single_col()
        self.find_single_box()
        self.update_possibles()

    def display_possiblities(self):
        """Displays possibilities for each cell for debugging"""
        for row in range(9):
            for col in range(9):
                print(f"{row} {col} {self.possibilities[row][col]}")

    def solve(self):
        """Begins the backtracking solving algorithm, but first places as many numbers as it can using simple logic above"""
        self.update_possibles()
        while self.changes:
            self.find_hidden_singles()
        self.put_number(0)

    def put_number(self, index):
        """
        Iterates through all cells of the grid, tries to place each number
        in turn into the cell and then looks for next non-empty cell.
        If a given solution is no longer valid, reverts the changes back up the recursive chain until it can continue again.
        """

        if self.solved:
            return
        row, col = index // 9, index % 9
        if row == 9 and self.is_valid():
            self.solved = True
            return
        if self.get_row_col(row, col) == 0:
            for x in range(1, 10):
                if self.is_possible(row, col, x):
                    self.set_row_col(row, col, x)
                    self.put_number(index+1)
                if not self.solved:
                    self.set_row_col(row, col, 0)
        else:
            self.put_number(index+1)


def main():
    #######################################
    # storing some test cases to be trialed
    array1 = [
        [0, 2, 0, 6, 0, 8, 0, 0, 0],
        [5, 8, 0, 0, 0, 9, 7, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [3, 7, 0, 0, 0, 0, 5, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 4],
        [0, 0, 8, 0, 0, 0, 0, 1, 3],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 9, 8, 0, 0, 0, 3, 6],
        [0, 0, 0, 3, 0, 6, 0, 9, 0]
    ]

    array2 = [
        [9, 8, 3, 0, 0, 0, 0, 4, 0],
        [0, 6, 0, 9, 0, 0, 0, 0, 8],
        [1, 0, 0, 0, 0, 8, 0, 6, 0],
        [0, 0, 0, 0, 0, 0, 9, 1, 0],
        [0, 0, 0, 5, 0, 6, 0, 0, 0],
        [3, 9, 6, 0, 0, 0, 8, 0, 2],
        [0, 0, 0, 4, 0, 5, 0, 0, 0],
        [5, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 8, 3, 0, 0, 0, 7, 4],
    ]

    array3 = [
        [3, 0, 9, 0, 0, 0, 4, 0, 0],
        [2, 0, 0, 7, 0, 9, 0, 0, 0],
        [0, 8, 7, 0, 0, 0, 0, 0, 0],
        [7, 5, 0, 0, 6, 0, 2, 3, 0],
        [6, 0, 0, 9, 0, 4, 0, 0, 8],
        [0, 2, 8, 0, 5, 0, 0, 4, 1],
        [0, 0, 0, 0, 0, 0, 5, 9, 0],
        [0, 0, 0, 1, 0, 6, 0, 0, 7],
        [0, 0, 6, 0, 0, 0, 1, 0, 4],
    ]
    unsolvable = [
        [3, 3, 9, 0, 0, 0, 4, 0, 0],
        [2, 0, 0, 7, 0, 9, 0, 0, 0],
        [0, 8, 7, 0, 0, 0, 0, 0, 0],
        [7, 5, 0, 0, 6, 0, 2, 3, 0],
        [6, 0, 0, 9, 0, 4, 0, 0, 8],
        [0, 2, 8, 0, 5, 0, 0, 4, 1],
        [0, 0, 0, 0, 0, 0, 5, 9, 0],
        [0, 0, 0, 1, 0, 6, 0, 0, 7],
        [0, 0, 6, 0, 0, 0, 1, 0, 4],
    ]
    sudoku = SudokuGrid(unsolvable)
    sudoku.solve()
    print(sudoku.solved)
    sudoku.display()

    sudoku1 = SudokuGrid(array1)
    sudoku1.find_hidden_singles()
    sudoku1.display()
    # print(sudoku1.solved)
    # sudoku1.display()

    ############################


if __name__ == '__main__':
    main()
