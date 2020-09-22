from tkinter import *
from tkinter import messagebox
from sudokugrid import SudokuGrid

NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
COL_LOGIC = '#FFA71A'  # Pale green colour
COL_BRUTE = '#2D6FE3'  # Blueish colour


class SudokuCanvas:
    def __init__(self, frame, initial, size):
        self.frame = frame
        self.WIDTH = size
        self.CELL_WIDTH = size // 9
        self.cell_text = [[{} for _ in range(9)] for _ in range(9)]
        self.cell_highlights = [[None for _ in range(9)] for _ in range(9)]
        self.solving = False
        self.canvas = Canvas(frame, width=size, height=size,
                             borderwidth=0, highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.5, anchor='center')
        self.guesses = [[{'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0,
                          '7': 0, '8': 0, '9': 0} for _ in range(9)] for _ in range(9)]
        self.curr_cell = None
        self.curr_cell_xy = None

        #  stores the players inputs
        self.sudoku = self.create_sudoku(initial)

        # stores the actual solution
        self.solution = self.create_sudoku(initial)

        # Drawing modes of 'DEFAULT','PENCIL','BIG'
        # Default: Draws big if only one number in the square, small if more than one
        # Pencil: Draws all numbers small
        # Big: Draws the number big, as if it is the only one
        self.draw_mode = 'DEFAULT'
        self.mode_string = StringVar()
        self.mode_string.set(f"Mode is: {self.draw_mode}")

        self.draw_grid()
        self.interactions()
        self.set_fixed_cells(initial)
        # self.solution.display()

    ##################################

    def visualize_solve(self):
        if not self.sudoku.solved:
            self.solving = True
        """Visualises the backtracking algorithm, 
        First checks for any cells which only have one possibility,
        then looks for values which can only be in one place in a given
        row/column/box.
        Once no single cells can be determined begins the backtracking step"""
        while self.sudoku.changes:
            self.sudoku.find_hidden_singles()
            for changed in self.sudoku.changes:
                row, col, x = changed
                for key in self.guesses[row][col].keys():
                    if int(key) != x:
                        self.guesses[row][col][key] = 0
                    else:
                        self.guesses[row][col][key] = 1
                self.update_cell(row, col)
                ind = self.cell_text[row][col][str(x)]
                self.canvas.itemconfig(ind, fill=COL_LOGIC)
                # highlight the cells solved in this way in some manor
                self.canvas.update()

        def put_number(index):
            """backtracking procedure, tries to place each
                possible number into a given cell. Then tries to place numbers
                in the next non-empty cell. If an attempted solution is no longer
                viable it will undo all placed numbers until it is back on a 
                viable solution"""
            row, col = index // 9, index % 9
            sudoku = self.sudoku
            if sudoku.solved:
                return
            self.canvas.update()
            if row == 9:
                self.sudoku.solved = True
                self.solving = False
                return
            else:
                if f"{row} {col}" in self.fixed_cells or sudoku.get_row_col(row, col) != 0:
                    put_number(index+1)
                else:
                    for x in range(1, 10):
                        if sudoku.is_possible(row, col, x):
                            for key in self.guesses[row][col].keys():
                                if int(key) != x:
                                    self.guesses[row][col][key] = 0
                                else:
                                    self.guesses[row][col][key] = 1
                            self.update_cell(row, col)
                            ind = self.cell_text[row][col][str(x)]
                            self.canvas.itemconfig(ind, fill=COL_BRUTE)
                            put_number(index+1)
                            if not self.sudoku.solved:
                                self.guesses[row][col][str(x)] = 0
                                self.update_cell(row, col)
        put_number(0)
    #####################################

    def create_sudoku(self, initial):
        array = [[0 for _ in range(9)] for _ in range(9)]
        for key, value in initial.items():
            row, col = [int(s) for s in key.split(" ")]
            array[row][col] = int(value)
        return SudokuGrid(array)

    def set_mode(self, mode):
        if mode in ['DEFAULT', 'PENCIL', 'BIG']:
            self.draw_mode = mode
            self.mode_string.set(f"Mode is: {self.draw_mode}")

    def toggle_mode(self, event=None):
        if self.solving:
            return
        mode = self.draw_mode
        if mode == 'DEFAULT':
            self.draw_mode = 'PENCIL'
        elif mode == 'PENCIL':
            self.draw_mode = 'BIG'
        elif mode == 'BIG':
            self.draw_mode = 'DEFAULT'
        self.mode_string.set(f"Mode is: {self.draw_mode}")

    def draw_grid(self):
        """draws the sudoku grid lines onto the canvas"""
        for i in range(1, 9):
            if i % 3 == 0:
                self.canvas.create_line(
                    0, i*self.CELL_WIDTH, self.WIDTH, i*self.CELL_WIDTH, fill='blue', width=2)
                self.canvas.create_line(
                    i*self.CELL_WIDTH, 0, i*self.CELL_WIDTH, self.WIDTH, fill='blue', width=2)
            else:
                self.canvas.create_line(
                    0, i*self.CELL_WIDTH, self.WIDTH, i*self.CELL_WIDTH, fill='gray')
                self.canvas.create_line(
                    i*self.CELL_WIDTH, 0, i*self.CELL_WIDTH, self.WIDTH, fill='gray')

    def interactions(self):
        """creates the control bindings"""
        self.canvas.bind("<Button-1>", self.select_cell)
        self.canvas.bind("<Left>", self.move_selection)
        self.canvas.bind("<Right>", self.move_selection)
        self.canvas.bind("<Up>", self.move_selection)
        self.canvas.bind("<Down>", self.move_selection)
        self.canvas.bind("<space>", self.toggle_mode)
        self.canvas.bind("<Key>", self.take_input)

    def set_fixed_cells(self, initial):
        """creates the cells which cannot be changed and creates the initial sudoku"""
        for row in range(9):
            for col in range(9):
                for num in NUMBERS:
                    self.guesses[row][col][num] = 0
                    self.update_cell(row, col)
        for key, value in initial.items():
            row, col = [int(s) for s in key.split(" ")]
            self.guesses[row][col][f"{value}"] = 1
            self.update_cell(row, col, 'bold')
        self.fixed_cells = initial
        self.sudoku = self.create_sudoku(initial)
        self.solution = self.create_sudoku(initial)
        # self.sudoku.display()
        self.solution.solve()
        if not self.solution.solved:
            messagebox.showwarning("Warning!", "No solution found")
        # self.solution.display()

    def draw_number(self, row, col, key, mode=None, font_weight=''):
        if mode is None:
            mode = self.draw_mode
        if mode == 'PENCIL':
            x_offset = (int(key) - 1) % 3 * (self.CELL_WIDTH//3-1) - 1
            y_offset = (int(key) - 1) // 3 * (self.CELL_WIDTH//3-1) - 1
            x_coord = col*self.CELL_WIDTH + x_offset
            y_coord = row*self.CELL_WIDTH + y_offset
            self.cell_text[row][col][key] = self.canvas.create_text(
                x_coord, y_coord, anchor='nw', text=f" {key} ")
        elif mode == 'BIG':
            x_coord = (col+0.5)*self.CELL_WIDTH
            y_coord = (row+0.5)*self.CELL_WIDTH
            self.cell_text[row][col][key] = self.canvas.create_text(
                x_coord, y_coord, text=f" {key} ", font=('TkDefaultFont', 24, font_weight))

    def update_cell(self, row, col, font_weight=''):
        """writes the value of all guesses into the [x,y]-th cell"""
        for key, value in self.guesses[row][col].items():
            # removes the number if no longer a guess
            if key in self.cell_text[row][col] and value == 0:
                self.canvas.delete(self.cell_text[row][col][key])
                self.cell_text[row][col].pop(key, None)
                if self.sudoku.get_row_col(row, col) == int(key):
                    self.sudoku.set_row_col(row, col, 0)
            # if it is a new guess draw the number
            if key not in self.cell_text[row][col] and value == 1:
                # rescales a large number if another number is added
                if len(self.cell_text[row][col]) == 1:
                    old, ind = list(self.cell_text[row][col].items())[0]
                    self.canvas.delete(ind)
                    self.draw_number(row, col, old, 'PENCIL', font_weight)
                    self.sudoku.set_row_col(row, col, 0)
                self.draw_number(row, col, key, 'PENCIL', font_weight)
        # makes the number large if it is the only entry into the cell
        if len(self.cell_text[row][col]) == 1:
            for key, value in self.cell_text[row][col].items():
                self.canvas.delete(value)
                if self.draw_mode == 'PENCIL':
                    self.draw_number(row, col, key, 'PENCIL', font_weight)
                else:
                    self.draw_number(row, col, key, 'BIG', font_weight)
                    self.sudoku.set_row_col(row, col, key)

    def move_selection(self, event):
        """ moves the currently highlighted cell in the direction pressed
            on the keyboard"""
        self.canvas.delete(self.curr_cell)
        curr_x, curr_y = self.curr_cell_xy[0], self.curr_cell_xy[1]
        if event.keysym == 'Up':
            new_x = curr_x
            new_y = (curr_y - self.CELL_WIDTH) % self.WIDTH
        elif event.keysym == 'Left':
            new_x = (curr_x-self.CELL_WIDTH) % self.WIDTH
            new_y = curr_y
        elif event.keysym == 'Down':
            new_x = curr_x
            new_y = (curr_y+self.CELL_WIDTH) % self.WIDTH
        elif event.keysym == 'Right':
            new_x = (curr_x+self.CELL_WIDTH) % self.WIDTH
            new_y = curr_y

        self.curr_cell = self.canvas.create_rectangle(
            new_x+1, new_y+1, new_x+self.CELL_WIDTH, new_y+self.CELL_WIDTH, fill='pink', outline="")
        self.curr_cell_xy = [new_x, new_y]
        self.canvas.tag_lower(self.curr_cell)

    def select_cell(self, event):
        """Highlights a cell on left mouseclick"""
        self.canvas.focus_set()
        if self.curr_cell:
            self.canvas.delete(self.curr_cell)
        # translates the x,y coords to indices of the grid, then scales them up
        top_left_x = event.x // self.CELL_WIDTH * self.CELL_WIDTH
        top_left_y = event.y // self.CELL_WIDTH * self.CELL_WIDTH
        # store in curr_cell the current rectangle ID and it's x,y coords in grid form
        self.curr_cell = self.canvas.create_rectangle(
            top_left_x+1, top_left_y+1, top_left_x+self.CELL_WIDTH, top_left_y+self.CELL_WIDTH, fill='pink', outline="")
        self.curr_cell_xy = [top_left_x, top_left_y]
        self.canvas.tag_lower(self.curr_cell)

    def take_input(self, event, button=False):
        if self.solving:
            return
        # allows me to pass through button presses instead
        if button:
            char = str(event)
        else:
            char = event.char
        if self.curr_cell is None:
            return

        col, row = self.curr_cell_xy[0] // self.CELL_WIDTH, self.curr_cell_xy[1] // self.CELL_WIDTH
        if f"{row} {col}" in self.fixed_cells:
            return
        if char in NUMBERS:
            if self.draw_mode == 'BIG':
                for key in self.guesses[row][col].keys():
                    self.guesses[row][col][key] = 0
            self.guesses[row][col][char] = (
                self.guesses[row][col][char] + 1) % 2
        # clears the cell of all numbers if you press c
        if char in ['c', 'C']:
            for num in NUMBERS:
                self.guesses[row][col][num] = 0
                self.sudoku.set_row_col(row, col, 0)
        # fills the cell with all possible values if you press f
        if char in ['f', 'F']:
            if self.draw_mode != 'BIG':
                for num in NUMBERS:
                    if self.sudoku.is_possible(row, col, int(num)):
                        self.guesses[row][col][num] = 1
                        self.sudoku.set_row_col(row, col, 0)
        self.update_cell(row, col)
