
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

let sudokuStructure = [];
let sudokuRows = [];
let sudokuColumns = [];
let sudokuBlocks = [];
let allCells = [];
let allFields = [];

parseExample = function (example, size) {
    for(let i = 0; i<size; i++) {
        for (let j = 0; j<size; j++) {
            const character = example.charAt(i*size+j)
            if (character != ' ') {
                sudokuStructure[i][j].setValue(parseInt(character));
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
    sudokuStructure = [];
    sudokuRows = [];
    sudokuColumns = [];
    sudokuBlocks = [];
    allCells = [];
    allFields = [];
    const table = document.getElementById("sudoku");
    table.innerHTML = "";
    for(let i = 0; i<size; i++) {
        sudokuStructure[i] = [];
        sudokuRows[i] = new Field();
        sudokuColumns[i] = new Field();
        sudokuBlocks[i] = new Field();
        allFields.push(sudokuRows[i]);
        allFields.push(sudokuColumns[i]);
        allFields.push(sudokuBlocks[i]);
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
            sudokuStructure[i][j] = cellObject;
            sudokuRows[i].addCell(cellObject);
            sudokuColumns[j].addCell(cellObject);
            sudokuBlocks[Math.floor(j/3)+3*Math.floor(i/3)].addCell(cellObject);
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
		bb.setAttribute("onClick", "setExample("+ex+")");
		buttons.appendChild(bb);
    }

    document.getElementById("solveOne").addEventListener("click", solveOne);
    document.getElementById("solveEasy").addEventListener("click", solveEasy);
    document.getElementById("solveAll").addEventListener("click", solveAll);
}

window.addEventListener("load", initsudoku);

class Cell {
    constructor(size, htmlElement, row, column, block) {
        this.options = Cell.getAllAvailabeOptions(size);
        this.htmlElement = htmlElement;
        this.showOptions();
        this.fields = [row, column, block];
    }

    static getAllAvailabeOptions(size) {
        return [...Array(size).keys()].map(x => x+1);
    }

    setValue(value) {
        this.htmlElement.innerHTML = value;
        this.value = value;
        this.options = [];
        this.htmlElement.classList.add("done");
        this.htmlElement.classList.add("new");
        this.fields.forEach(field => field.removeOption(value))
    }

    removeOption(optionToRemove) {
        if (this.value) return;
        this.options = this.options.filter(option => optionToRemove !== option);
        this.showOptions();
    }

    setHint() {
        this.htmlElement.classList.add("hint");
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
                this.removeOption([option]);
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

class Field {
    constructor () {
        this.cells = [];
    }

    addCell(cell) {
        this.cells.push(cell);
    }

    removeOption(option) {
        this.cells.forEach(cell => cell.removeOption(option))
    }

    checkLonelyNumbers() {
        console.log(this.cells.length)
        for (const option of Cell.getAllAvailabeOptions(this.size)) {
            let count = 0;
            let theCell;
            for (const cell of this.cells) {
                if (cell.options.includes(option)) {
                    theCell=cell;
                    count++;
                }
            }
            if (count == 1 && ! theCell.value) {
                displayStatus("only one cell possible for " + option);
                for (const cell of this.cells) cell.setHint();
                theCell.setValue(option);
                return true;
            }
        }
        return false;
    }
}

function solve(stopAtDifficulty, keepGoing) {
    for (const cell of allCells) {
        cell.dropTempClasses();
    }

    foundSomething = false;
    difficultyReached = 0;

    // break out of this code block if we've found something
    // or further attempts are too hard
    solveAttempts : {
        difficultyReached = 1;
        for (const cell of allCells) {
            if (cell.checkOne()) {
                foundSomething = true;
                break solveAttempts;
            }
        }

        difficultyReached = 2;
        console.log(allFields.length);
        for (const field of allFields) {
            if (field.checkLonelyNumbers()) {
                foundSomething = true;
                break solveAttempts;
            }
        }

        difficultyReached = 3;

        // more solve attempts to be translated from previous version
    }

    if (foundSomething 
        && keepGoing
        && stopAtDifficulty > difficultyReached) {
        setTimeout(
            () => solve(stopAtDifficulty, keepGoing),
            100
        );
    }

}

function solveOne() {
    solve(100, false);
}

function solveEasy() {
    solve(2, true);
}

function solveAll() {
    solve(100, true);
}