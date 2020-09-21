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

    def set_row_col(self, row, col, x):
        try:
            self.array[row][col] = int(x)
            self.possibilities[row][col] = {}
        except:
            print(f"Didn't input an integer {x} {type(x)}")

    def get_row_col(self, row, col):
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
        errors = []
        for row in range(9):
            for col in range(9):
                if not self.is_possible(row, col):
                    errors.append([row, col])
        if errors != []:
            return errors
        else:
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

    def solve(self):
        """Begins solving by a backtracking method"""
        self.put_number(0)

    def put_number(self, index):
        row, col = index // 9, index % 9

        if self.solved:
            return
        if row == 9:
            self.solved = True
            return
        else:
            if self.get_row_col(row, col) == 0:
                for x in range(1, 10):
                    if self.is_possible(row, col, x):
                        self.set_row_col(row, col, x)
                        self.put_number(index+1)
                        # this check ensures that it doesn't revert the solution to the original state in the case it finds a solution
                        if not self.solved:
                            self.set_row_col(row, col, 0)
            else:
                self.put_number(index+1)


# for the next part want to try to optimise the backtrack algorithm
# create a possibility array for each point - consisting of the numbers that a cell could be
# then want to iterate through the rows,columns and box
# if a value only appears in one cell in a row or a column or a box then set the value in the sudoku to that
    # when any value is placed re-eliminate possibilities
# then adapt the backtracking algoirthm so that it does this check at every stage?


    def init_possibles(self):
        # for each cell create a dictionary consisting of possible values
        # chose a dictionary for ease of deleting and accessing values
        possibilities = [[{} for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                if f"{row} {col}" in self.initial_values:
                    x = self.get_row_col(row, col)
                    possibilities[row][col][f"{x}"] = x
                else:
                    for x in range(1, 10):
                        if self.is_possible(row, col, x):
                            possibilities[row][col][f"{x}"] = x
        return possibilities

    def update_possibles(self):
        for row in range(9):
            for col in range(9):
                to_remove = []
                for key in self.possibilities[row][col].keys():
                    if not self.is_possible(row, col, int(key)):
                        to_remove += key
                for key in to_remove:
                    self.possibilities[row][col].pop(key, None)

    def find_single_row(self):
        # for each row will count how many times each value appears
        # if it only appears once in a row then we set the value
        for row in range(9):
            for x in range(1, 10):
                value = str(x)
                value_count = 0  # counts how much the value appears in a row
                value_row_cols = []
                for col in range(9):
                    if value in self.possibilities[row][col]:
                        value_count += 1
                        value_row_cols.append([row, col])
                if value_count == 1:
                    row, col = value_row_cols[0]
                    self.set_row_col(row, col, x)
                    self.changes += 1
        self.update_possibles

    def find_single_col(self):
        # does same as above except checks for column singles
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
                    self.changes += 1
        self.update_possibles()

    def find_single_box(self):
        # checks for singles in each box
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
                    self.changes += 1
        self.update_possibles()

    def find_hidden_singles(self):
        self.changes = 0
        self.find_single_row()
        self.find_single_col()
        self.find_single_box()

    def solve_better(self):
        """Begins the solving algorithm"""
        self.changes = True
        self.put_number_better(0)

    def put_number_better(self, index):
        """
        Solves the sudoku by first trying to find any numbers which must be placed into the grid
        (by seeing that there is only one space in a row to place a number).
        Once all of these are placed it begins a backtracking algorithm, looping through the cells and 
        placing a value in a given cell. Once it places a number it looks for singles again.
        """

        # Need to be able to undo the changes caused by searching for hidden singles

        while(self.changes):
            self.find_hidden_singles()
        if self.solved:
            return
        row, col = index // 9, index % 9
        if row == 9 and self.is_valid():
            self.solved = True
            return
        if self.get_row_col(row, col) == 0:
            for x in self.possibilities[row][col].items():
                self.set_row_col(row, col, x)
                self.put_number_better(index+1)
                if not self.solved:
                    self.set_row_col(row, col, 0)
        else:
            self.put_number_better(index+1)


array1 = [
    [0, 5, 0, 0, 2, 0, 3, 0, 1],
    [0, 0, 0, 6, 5, 1, 0, 0, 8],
    [1, 7, 2, 0, 0, 0, 6, 4, 5],
    [0, 9, 0, 0, 0, 0, 5, 3, 0],
    [2, 0, 0, 5, 0, 4, 0, 0, 6],
    [8, 0, 0, 0, 3, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 0, 0, 9, 6, 5, 0, 1, 0],
    [0, 6, 0, 0, 0, 2, 9, 0, 0],
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


############################

sudoku1 = SudokuGrid(array1)
sudoku2 = SudokuGrid(array2)
# for row in range(9):
#     for col in range(9):
#         print(f"{row} {col} {sudoku.possibilities[row][col]}")
# while(input() != '-1'):
#     sudoku.find_hidden_singles()

# start = time.time()
# sudoku.solve()
# print(time.time()-start)
# print(sudoku.is_valid())
# sudoku.display()

start = time.time()
sudoku1.solve_better()
print(time.time()-start)
print(sudoku1.is_valid())
sudoku1.display()

start = time.time()
sudoku2.solve_better()
print(time.time()-start)
print(sudoku2.is_valid())
sudoku2.display()
