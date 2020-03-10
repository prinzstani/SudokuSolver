# Sudoku Solver
This **Sudoku Solver** is a web page that allows you to type your sudoku problems, and that will help you solve them.
The solver follows a human-centered approach by applying rules all the way.
It will also indicate which rules are used during the solving process.
There is no guessing involved in the process, and sometimes the solver does not find any applicable rules and cannot solve the problem.

## Current version

You can run the current version at the [run page](https://prinzstani.github.io/SudokuSolver/Web/sudoku.html).

You find the code for the current version [at the repository](https://github.com/prinzstani/SudokuSolver).

## What it does

Sudoku solver simply solves [sudoku puzzles](https://en.wikipedia.org/wiki/Sudoku). It applies a number of rules that also human solvers would apply. If no more rules are applicable, the solving process fails.
The solving process emplys a notion of field, which could be a row, a block, or a column of the sudoku. The following rules are implemented.

### Simple rules
The solver employs the following simple rules for reducing the number of options.
* If a number is correct in a cell, it is impossible in any other cell of the same field.
* If there is only one option for a cell, this is the correct number.
* If there is only one cell in a field for some number, then this number has to be in this cell.

### Shared cells between fields
If two fields share more than 1 cell, and for one field, some number only appears in the shared cells, then also for the other field, this number can only appear in the shared fields.

Example: Consider a block and a row that overlap in their first three cells with the following options:
* block: (12) (13) (14) (1245) (16) (67) (45678) (4789) (4679)
* row: (12) (13) (14) (2345) (2346) (23467) (478) (4789) (589)

Now the row has the 1 only in the shared cells, such that in the block, also the cells with 1 outside the shared cells have to be removed. This will remove the 1 from the alternative (16), and this will trigger another rule.

### Complete groups of alternatives
If there are n cells within a field that together only have n alternatives for their numbers, then this number cannot appear in any other cell in the same field.

Example: Consider a field with the following cell options: (12) (23) (13) (34) (45) (569) (679) (789) (89). Here, (12), (23), (13) are three cells that together only have three options (123), which means that (123) cannot appear anywhere else. This again means that the option (34) has to be reduced to (4), which triggers another rule.

# Bugs and suggestions

Any bug or suggestion should be **created as an issue** [in the repository](https://github.com/prinzstani/SudokuSolver/issues) for easier tracking. This allows to follow the status of the issue.

All suggestions are welcome, even the smallest ones.

# Contributors
* See the [list of commit contributors](https://github.com/prinzstani/SudokuSolver/graphs/contributors)
