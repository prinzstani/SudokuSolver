
const examples = ["6   7 4 1"+" 7   298 "+"     65  "+"73   9  4"+"  261  78"+"    8    "+" 4 96 7 3"+" 8  53 42"+" 5    8  ",
				  "    3   4"+"16 57 2  "+" 3   1  8"+"  9      "+"78 3 4 95"+"      1  "+"9  6   4 "+"  3 59 27"+"8   1    ",
				  " 628   3 "+"  5  7  8"+"  4 9   6"+"4    9   "+"  7   5  "+"   2    1"+"8   5 7  "+"5  9  1  "+" 2   465 ",
				  "4      9 "+"18  5 3  "+"  3   2  "+"   73  1 "+"94   8   "+"7     9  "+" 7   6   "+"  6   7 5"+"8   4    ",
				  "  9  7 8 "+"83       "+" 1 6    7"+"    48  1"+"  6 3 8  "+"9  15    "+"2    1 6 "+"       54"+" 6 3  7  ",
				  " 2   1   "+" 5 8   1 "+"   4 23  "+"4    7298"+"5       1"+" 39   4  "+"  3 45 6 "+"         "+"  8 6    ",
				  "  2 4    "+" 5  7  3 "+"4 3  6  8"+"     95 1"+" 4  8  7 "+"1 67     "+"5  8  2 6"+" 6  3  5 "+"    2 8  "];

setExample = function (idx) {
    init(9);
    parseExample(examples[idx], 9);
}

let sudokuRows = [];
let sudokuColumns = [];
let sudokuBlocks = [];
let allCells = [];

parseExample = function (example, size) {
    for(let i = 0; i<size; i++) {
        for (let j = 0; j<size; j++) {
            const character = example.charAt(i*size+j)
            if (character != ' ') {
                sudokuRows[i][j].setValue(parseInt(character));
            }
        }
    }
	displayStatus("Let's solve example: "+ example);
}

displayStatus = function (str) {
	const status = document.getElementById("status");
    status.innerHTML = str;
}

init = function(size) {
    sudokuRows = [];
    sudokuColumns = [];
    sudokuBlocks = [];
    allCells = [];
     const table = document.getElementById("sudoku");
    table.innerHTML = "";
    for(let i = 0; i<size; i++) {
        sudokuRows[i] = [];
        sudokuColumns[i] = [];
        sudokuBlocks[i] = [];
    }

    for(let i = 0; i<size; i++) {
        const row = document.createElement("tr");
        for (let j = 0; j<size; j++) {
            const cell = document.createElement("td");
            cell.id = "cell_" + i + "_" + j;
            row.appendChild(cell);
            const cellObject = new Cell(
                size,
                cell,
                sudokuRows[i],
                sudokuColumns[j],
                sudokuBlocks[Math.floor(j/3)+3*Math.floor(i/3)]
            )
            sudokuRows[i][j] = cellObject;
            sudokuColumns[j][i] = cellObject;
            sudokuBlocks[Math.floor(j/3)+3*Math.floor(i/3)].push(cellObject);
            allCells.push(cellObject);
        }
        table.appendChild(row);
    }
}

initsudoku = function() {
    const buttons = document.getElementById("control");

	init(9);
	for (ex in examples) {
		const bb = document.createElement("button");
		bb.innerHTML = "Example " + (parseInt(ex)+1);
		bb.addEventListener("click", () => setExample(ex));
		buttons.appendChild(bb);
    }

    document.getElementById("solveOne").addEventListener("click", solveOne);
    document.getElementById("solveEasy").addEventListener("click", solveEasy);
    document.getElementById("solveAll").addEventListener("click", solveAll);
}

window.addEventListener("load", initsudoku);

class Cell {
    constructor(size, htmlElement, row, column, block) {
        this.options = [...Array(size).keys()].map(x => x+1);
        this.htmlElement = htmlElement;
        this.showOptions();
        this.row = row;
        this.block = block;
        this.column = column;
    }

    setValue(value) {
        this.htmlElement.innerHTML = value;
        this.value = value;
        this.options = [];
        this.htmlElement.classList.add("done");
        this.htmlElement.classList.add("new");
        for (let otherCell of this.row) {
            otherCell.removeOptions([value]);
        }
        for (let otherCell of this.column) {
            otherCell.removeOptions([value]);
        }
        for (let otherCell of this.block) {
            otherCell.removeOptions([value]);
        }
    }

    removeOptions(optionsToRemove) {
        if (this.value) return;
        this.options = this.options.filter(option => !optionsToRemove.includes(option));
        this.showOptions();
    }

    checkOne() {
        if (this.value) return;
        if (this.options.length === 1) {
            const value = this.options[0];
            this.setValue(value);
            displayStatus("only one possibility left: " + value);
            return true;
        }
        return false;
    }

    showOptions() {
        this.htmlElement.innerHTML = "";
        const optionsContainer = document.createElement("div");
        optionsContainer.classList = ["options"];
        this.options.map(option => {
            const optionDiv = document.createElement("div");
            optionDiv.innerHTML = option;
            optionDiv.addEventListener("click", () => {
                this.removeOptions([option]);
            });
            optionsContainer.appendChild(optionDiv);
        })
        this.htmlElement.appendChild(optionsContainer);
    }

    dropTempClasses() {
        this.htmlElement.classList.remove("new");
        this.htmlElement.classList.remove("hint");
    }
}

function solve(stopAtDifficulty) {
    for (const cell of allCells) {
        cell.dropTempClasses();
    }

    for (const cell of allCells) {
        if (cell.checkOne()) {
            return;
        }
    }
}

function solveOne() {
    solve(0);
}

function solveEasy() {
    solve(2);
}

function solveAll() {
    solve(100);
}