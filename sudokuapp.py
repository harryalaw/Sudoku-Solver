from tkinter import *
from sudokucanvas import SudokuCanvas

NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']


class App(Frame):
    def __init__(self, master):
        super(App, self).__init__(master)
        self.master = master

        # will keep track of the initial set up of the sudoku grid
        # self.initial = {"1 0": '2', "3 0": '6', "5 0": '8', "0 1": '5', "1 1": '8', '5 1': '9', "6 1": '7', "4 2": '4', "0 3": '3', '1 3': '7', '6 3': '5',
        # '0 4': '6', '8 4': '4', '2 5': '8', '7 5': '1', '8 5': '3', '4 6': '2', '2 7': '9', '3 7': '8', '7 7': '3', '8 7': '6', '3 8': '3', '5 8': '6', '7 8': '9'}
        self.initial = {'0 1': '5', '0 4': '2', '0 6': '3', '0 8': '1', '1 3': '6', '1 4': '5', '1 5': '1', '1 8': '8', '2 0': '1', '2 1': '7', '2 2': '2', '2 6': '6', '2 7': '4', '2 8': '5', '3 1': '9',
                        '3 6': '5', '3 7': '3', '4 0': '2', '4 3': '5', '4 5': '4', '4 8': '6', '5 0': '8', '5 4': '3', '5 7': '2', '7 0': '7', '7 3': '9', '7 4': '6', '7 5': '5', '7 7': '1', '8 1': '6', '8 5': '2', '8 6': '9'}

        self.create_widgets()

    def create_widgets(self):
        master = self.master
        Grid.columnconfigure(master, 0, weight=2)
        Grid.columnconfigure(master, 1, weight=1)
        self.sudoku_frame = Frame(master, bg='white', width=400, height=400)
        self.numpad_frame = Frame(master, bg='white', width=200, height=200)
        self.control_frame = Frame(master, bg='white', width=200, height=100)
        self.options_frame = Frame(master, bg='white', width=200, height=100)

        self.sudoku_frame.grid(row=0, column=0, rowspan=3, sticky='news')
        self.numpad_frame.grid(row=0, column=1, sticky='news')
        self.control_frame.grid(row=1, column=1, sticky='news')
        self.options_frame.grid(row=2, column=1, sticky='news')

        self.init_canvas()
        self.init_numpad()
        self.init_controls()

        self.init_options()

    def init_canvas(self):
        self.sub_frame = Frame(
            self.sudoku_frame, bg='black', width=362, height=362)
        self.sub_frame.place(relx=0.5, rely=0.5, anchor='center')
        self.sudoku_canvas = SudokuCanvas(self.sub_frame, self.initial, 360)

    def init_numpad(self):
        self.bttn_frame = Frame(self.numpad_frame)
        self.bttn_frame.place(relx=0.5, rely=0.5, anchor='center')
        self.buttons = []
        for i in range(9):
            new_bttn = Button(self.bttn_frame, text=str(i+1),
                              width=4, height=2)
            self.buttons.append(new_bttn)
        self.fill_bttn = Button(
            self.bttn_frame, text='Fill cell', width=14, height=1,
            command=lambda value='f', button=True: self.sudoku_canvas.take_input(value, button))
        self.clear_bttn = Button(
            self.bttn_frame, text='Clear cell', width=14, height=1,
            command=lambda value='c', button=True: self.sudoku_canvas.take_input(value, button))

        for i, bttn in enumerate(self.buttons):
            bttn.grid(row=i//3, column=i % 3)
            # we abuse the description of take_input to pass through value as the event tag in the take_input function
            bttn.config(command=lambda value=i+1,
                        button=True: self.sudoku_canvas.take_input(value, button))
        self.fill_bttn.grid(row=3, columnspan=3)
        self.clear_bttn.grid(row=4, columnspan=3)

    def init_controls(self):
        self.toggle_mode_bttn = Button(
            self.control_frame, textvariable=self.sudoku_canvas.mode_string, command=self.sudoku_canvas.toggle_mode, width=18)
        self.toggle_mode_bttn.pack()

    def init_options(self):

        def reveal_cell():
            if self.sudoku_canvas.curr_cell_xy is None or self.sudoku_canvas.solving:
                return
            col, row = [
                int(s) // self.sudoku_canvas.CELL_WIDTH for s in self.sudoku_canvas.curr_cell_xy]
            true_value = str(self.sudoku_canvas.solution.get_row_col(row, col))
            prev_mode = self.sudoku_canvas.draw_mode
            self.sudoku_canvas.set_mode('BIG')
            self.sudoku_canvas.take_input(true_value, True)
            self.sudoku_canvas.fixed_cells[f"{row} {col}"] = true_value
            self.sudoku_canvas.set_mode(prev_mode)

        def reset_canvas():
            if self.sudoku_canvas.solving:
                return
            self.sudoku_canvas.set_fixed_cells({})
            self.sudoku_canvas.set_mode('BIG')
            self.new_grid_bttn.config(
                text='Set Grid', command=set_sudoku)

        def set_sudoku():
            if self.sudoku_canvas.solving:
                return
            initial = {}
            for row in range(9):
                for col in range(9):
                    for key, value in self.sudoku_canvas.guesses[row][col].items():
                        if value != 0:
                            # using a row column notation
                            initial[f"{row} {col}"] = key
            self.sudoku_canvas.set_fixed_cells(initial)
            self.sudoku_canvas.set_mode('DEFAULT')
            # print(initial)

            self.new_grid_bttn.config(
                text='New Grid', command=reset_canvas)

        def solve_grid():
            if self.sudoku_canvas.solving:
                return
            self.sudoku_canvas.visualize_solve()

        def error_check():
            if self.sudoku_canvas.solving:
                return
            for row in range(9):
                for col in range(9):
                    curr_val = self.sudoku_canvas.sudoku.get_row_col(row, col)
                    true_val = self.sudoku_canvas.solution.get_row_col(
                        row, col)
                    if int(curr_val) == 0:
                        continue
                    elif int(curr_val) != int(true_val):
                        for key, value in self.sudoku_canvas.cell_text[row][col].items():
                            self.sudoku_canvas.canvas.itemconfig(
                                value, fill='red')

        self.new_grid_bttn = Button(
            self.options_frame, text='New Grid', command=reset_canvas, width=18)
        self.check_bttn = Button(
            self.options_frame, text='Check For Errors', command=error_check, width=18)
        self.reveal_bttn = Button(
            self.options_frame, text='Reveal Cell', command=reveal_cell, width=18)
        self.solve_bttn = Button(
            self.options_frame, text='Solve Grid', command=solve_grid, width=18)

        self.new_grid_bttn.pack(anchor='center')
        self.check_bttn.pack(anchor='center')
        self.reveal_bttn.pack(anchor='center')
        self.solve_bttn.pack(anchor='center')


root = Tk()
window = App(root)

window.mainloop()
