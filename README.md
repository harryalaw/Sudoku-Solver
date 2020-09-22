# Sudoku-Solver

To run: python sudokuapp.py

An app where you can input your own sudoku puzzles and either solve them yourself or have them solved via an algorithm based on backtracking. 

# Controls

Select a cell on the grid with a click to highlight a cell. 
Can then use the arrow keys to move the highlighted cell around.

Can input a number onto the grid by either using the buttons on the right hand side of the app, or by pressing the corresponding numerical key.

Pressing 'f' or 'c' fills or clears respectively the currently selected of all possible guesses.
## Drawing modes
The drawing mode determines how the users inputs are represented on the board. In default mode, if only one value is entered into a cell then it occupies the whole cell, but if more than one number is input then it makes all inputted numbers pencil marks.

In pencil mode, all inputs are rendered as pencil marks.

In both pencil and default mode a number can be removed by pressing the same value again, i.e. a 1 can be removed from a cell by trying to input 1 to it.

In big mode any inputted number occupies the whole square. If you change the input then the new number occupies the whole square. No pencil marks will be created. To clear a cell in this mode press 'c' or the clear cell button.

Can cycle through the modes either by pressing spacebar or by clicking the button.

## Options
New grid: clears the current initial pattern and allows the user to setup a new sudoku puzzle to be solved.
In this mode all inputs act as if they are in the big drawing mode. Can press set grid to fix all inputted values and begin solving. The puzzle will then be solved before the user can interact with the sudoku again.

Check for errors: checks all current inputs for any values which do not match the solution found in creation of the grid.

Reveal cell: Takes the current highlighted cell and displays the value found in the solution

Solve grid: Provides a visualisation of how the algorithm solved the puzzle. 
