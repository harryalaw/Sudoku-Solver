from itertools import product


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
        except:
            print(f"Didn't input an integer {x} {type(x)}")

    def get_row_col(self, row, col):
        return self.array[row][col]

    def set_initial_values(self):
        """stores the initial values in the form of [[row,col], value]"""
        initial_values = []
        for i in range(9):
            for j in range(9):
                if self.get_row_col(i, j) != 0:
                    initial_values.append([[i, j], self.get_row_col(i, j)])
        return initial_values

    def init_possibles(self):
        # for each cell create a dictionary consisting of possible values
        # chose a dictionary for ease of deleting and accessing values
        possibilities = [[{} for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                for x in range(9):
                    if self.is_possible(row, col, x):
                        possibilities[row][col][f"{x}"] = 1
        return possibilities

    def update_possibles(self):
        for row in range(9):
            for col in range(9):
                for key in self.is_possible(row, col).keys():
                    if not self.is_possible(row, col, int(key)):
                        self.possibilities[row][col].pop(key, None)

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

        def find_naked_singles_row(self):
            # for each row will count how many times each value appears
            # if it only appears once in a row then we set the value
            for row in range(9):
                for x in range(9):
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
