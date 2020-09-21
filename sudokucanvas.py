from tkinter import *
from sudokugrid import SudokuGrid

NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']


class SudokuCanvas:
    def __init__(self, frame, initial, size):
        self.frame = frame
        self.WIDTH = size
        self.CELL_WIDTH = size // 9
        self.cell_text = [[{} for _ in range(9)] for _ in range(9)]

        self.canvas = Canvas(frame, width=size, height=size,
                             borderwidth=0, highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.5, anchor='center')
        self.guesses = [[{'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0,
                          '7': 0, '8': 0, '9': 0} for _ in range(9)] for _ in range(9)]
        self.curr_cell = None
        self.curr_cell_xy = None

        self.sudoku = self.create_sudoku(initial)  #  stores the players inputs
        self.solution = self.create_sudoku(
            initial)  # stores the actual solution

        # Will have drawing modes of 'DEFAULT','PENCIL','BIG'
        # Default: Draws big if only one number in the square, small if more than one
        # Pencil: Draws all numbers small
        # Big: Draws the number big, as if it is the only one
        self.draw_mode = 'DEFAULT'
        self.mode_string = StringVar()
        self.mode_string.set(f"Current mode is: {self.draw_mode}")

        self.draw_grid()
        self.interactions()
        self.set_fixed_cells(initial)
        self.solution.display()

    ##################################

    def visualize_solve(self):

        def put_number(index):
            row, col = index // 9, index % 9
            sudoku = self.sudoku
            if sudoku.solved:
                return
            self.canvas.update()
            if row == 9:
                self.sudoku.solved = True
                return
            else:
                if f"{col} {row}" in self.fixed_cells or sudoku.get_row_col(row, col) != 0:
                    put_number(index+1)
                else:
                    for x in range(1, 10):
                        if sudoku.is_possible(row, col, x):
                            for key in self.guesses[row][col].keys():
                                if int(key) != x:
                                    self.guesses[row][col][key] = 0
                                else:
                                    self.guesses[row][col][key] = 1
                                self.update_cell(col, row)
                            put_number(index+1)
                            if not self.sudoku.solved:
                                self.guesses[row][col][str(x)] = 0
                            self.update_cell(col, row)
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
            self.mode_string.set(f"Current mode is: {self.draw_mode}")

    def toggle_mode(self, event=None):
        mode = self.draw_mode
        if mode == 'DEFAULT':
            self.draw_mode = 'PENCIL'
        elif mode == 'PENCIL':
            self.draw_mode = 'BIG'
        elif mode == 'BIG':
            self.draw_mode = 'DEFAULT'
        self.mode_string.set(f"Current mode is: {self.draw_mode}")

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
        for y in range(9):
            for x in range(9):
                for num in NUMBERS:
                    self.guesses[y][x][num] = 0
                    self.update_cell(x, y)
        for key, value in initial.items():
            x, y = [int(s) for s in key.split(" ")]
            self.guesses[y][x][f"{value}"] = 1
            self.update_cell(x, y, 'bold')
        self.fixed_cells = initial
        self.sudoku = self.create_sudoku(initial)
        self.solution = self.create_sudoku(initial)
        self.sudoku.display()
        self.solution.solve()
        self.solution.display()

    def draw_number(self, x, y, key, mode=None, font_weight=''):
        if mode is None:
            mode = self.draw_mode
        if mode == 'PENCIL':
            x_offset = (int(key) - 1) % 3 * (self.CELL_WIDTH//3-1) - 1
            y_offset = (int(key) - 1) // 3 * (self.CELL_WIDTH//3-1) - 1
            x_coord = x*self.CELL_WIDTH + x_offset
            y_coord = y*self.CELL_WIDTH + y_offset
            self.cell_text[y][x][key] = self.canvas.create_text(
                x_coord, y_coord, anchor='nw', text=f" {key} ")
        elif mode == 'BIG':
            x_coord = (x+0.5)*self.CELL_WIDTH
            y_coord = (y+0.5)*self.CELL_WIDTH
            self.cell_text[y][x][key] = self.canvas.create_text(
                x_coord, y_coord, text=f" {key} ", font=('TkDefaultFont', 24, font_weight))

    def update_cell(self, x, y, font_weight=''):
        """writes the value of all guesses into the [x,y]-th cell"""
        for key, value in self.guesses[y][x].items():
            # removes the number if no longer a guess
            if key in self.cell_text[y][x] and value == 0:
                self.canvas.delete(self.cell_text[y][x][key])
                self.cell_text[y][x].pop(key, None)
                if self.sudoku.get_row_col(y, x) == int(key):
                    self.sudoku.set_row_col(y, x, 0)
            # if it is a new guess draw the number
            if key not in self.cell_text[y][x] and value == 1:
                # rescales a large number if another number is added
                if len(self.cell_text[y][x]) == 1:
                    old, ind = list(self.cell_text[y][x].items())[0]
                    self.canvas.delete(ind)
                    self.draw_number(x, y, old, 'PENCIL', font_weight)
                    self.sudoku.set_row_col(y, x, 0)
                self.draw_number(x, y, key, 'PENCIL', font_weight)
        # makes the number large if it is the only entry into the cell
        if len(self.cell_text[y][x]) == 1:
            for key, value in self.cell_text[y][x].items():
                self.canvas.delete(value)
                if self.draw_mode == 'PENCIL':
                    self.draw_number(x, y, key, 'PENCIL', font_weight)
                else:
                    self.draw_number(x, y, key, 'BIG', font_weight)
                    self.sudoku.set_row_col(y, x, key)

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
        # allows me to pass through button presses instead
        if button:
            char = str(event)
        else:
            char = event.char
        if self.curr_cell is None:
            return

        x, y = self.curr_cell_xy[0] // self.CELL_WIDTH, self.curr_cell_xy[1] // self.CELL_WIDTH
        if f"{x} {y}" in self.fixed_cells:
            return
        if char in NUMBERS:
            if self.draw_mode == 'BIG':
                for key in self.guesses[y][x].keys():
                    self.guesses[y][x][key] = 0
            self.guesses[y][x][char] = (self.guesses[y][x][char] + 1) % 2
        # clears the cell of all numbers if you press c
        if char in ['c', 'C']:
            for num in NUMBERS:
                self.guesses[y][x][num] = 0
                self.sudoku.set_row_col(y, x, 0)
        # fills the cell with all possible values if you press f
        if char in ['f', 'F']:
            if self.draw_mode != 'BIG':
                for num in NUMBERS:
                    self.guesses[y][x][num] = 1
                    self.sudoku.set_row_col(y, x, 0)
        self.update_cell(x, y)
