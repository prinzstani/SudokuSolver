// sudoku solver - most possible human

const examples = ["9x9-6...7.4.1.7...298......65..73...9..4..261..78....8.....4.96.7.3.8..53.42.5....8..-",
				  "9x9-....3...416.57.2...3...1..8..9......78.3.4.95......1..9..6...4...3.59.278...1....-",
				  "9x9-.628...3...5..7..8..4.9...64....9.....7...5.....2....18...5.7..5..9..1...2...465.-",
				  "9x9-4......9.18..5.3....3...2.....73..1.94...8...7.....9...7...6.....6...7.58...4....-",
				  "9x9-..9..7.8.83........1.6....7....48..1..6.3.8..9..15....2....1.6........54.6.3..7..-",
				  "9x9-.2...1....5.8...1....4.23..4....72985.......1.39...4....3.45.6............8.6....-",
				  "9x9-..2.4.....5..7..3.4.3..6..8.....95.1.4..8..7.1.67.....5..8..2.6.6..3..5.....2.8..-",
				  "9x9-4..76.9.2.79.28...............8...63..29.31..34...6...............15.78.5.1.87..9-",
				  "9x9-3.7..64..5..24.....64.5.....18....2..5..6..9..4....57.....2.84.....18..9..96..2.3-",
				  "9x9diagonal-.9.....4.4..7..1.3...95..7..89........4...2........75..6..72...2.8..6..5.4.....2.-"];

getSudokuString = function() {
    sudokuString = window.location.href.split('?')[0];
    sudokuString += '?puzzle='
    sudokuString += gridSize + 'x' + gridSize;
    sudokuString += gridDiagonals ? 'diagonal' : '';
    sudokuString += '-';
    for (row of sudokuStructure) {
        for (cell of row) {
            sudokuString += cell.initial ? cell.value : '.';
        }
    } 
    sudokuString += '-';
    console.log(sudokuString);
    navigator.clipboard.writeText(sudokuString);
}

readSudokuString = function(sudokuString) {
    [identifier, content] = sudokuString.split('-');
    [size, type] = identifier.split('x');
    type = type.replace(size, '');
    size = parseInt(size);
    gridDiagonals = (type == "diagonal");
    init(size, false);
    parseExample(content, size);
}

let sudokuStructure = [];
let gridSize = 9;
let gridDiagonals = false;
let addDiagonalsWhenNew = false;
let sudokuRows = [];
let sudokuColumns = [];
let sudokuBlocks = [];
let sudokuDiagonals = [];
let allCells = [];
let allFields = [];

parseExample = function (example, size) {
    for(let i = 0; i<size; i++) {
        for (let j = 0; j<size; j++) {
            const character = example.charAt(i*size+j)
            if (character > '0' && character <= '9') {
                sudokuStructure[i][j].setValue(parseInt(character), true);
            }
        }
    }
	displayStatus("Let's solve example: "+ example);
}

displayStatus = function (str) {
	const status = document.getElementById("status");
    status.innerHTML = str;
}

let selectOptionOnClick;

updateOptionClickResult = function() {
    const selectedRadioButton = document.querySelector('input[name="clickResult"]:checked');
    selectOptionOnClick = selectedRadioButton.value === "true";
}

let selectAsInitial;

updateSelectAsInitial = function() {
    const checkBox = document.getElementById("setAsInitial");
    selectAsInitial = checkBox.checked;
}

let solveAllWhenSelecting;

updateSolveAllWhenSelecting = function() {
    const checkBox = document.getElementById("solveWhenSelecting");
    solveAllWhenSelecting = checkBox.checked;
}

updateOptions = function() {
    updateOptionClickResult();
    updateSelectAsInitial();
    updateSolveAllWhenSelecting();
}

updateDiagonals = function() {
    const checkBox = document.getElementById("diagonals");
    addDiagonalsWhenNew = checkBox.checked;
}

init = function(size = gridSize, newGridType = false) {
    gridSize = size;
    if (newGridType) {
        gridDiagonals = addDiagonalsWhenNew;
        diagonalContainer = document.getElementById("diagonalContainer");
    }
    if (gridDiagonals) {
        diagonalContainer.classList.remove("hide");
    } else {
        diagonalContainer.classList.add("hide");
    }
    let xPeriod = Math.sqrt(size);
    let yPeriod = Math.sqrt(size);
    if (size === 6) {
        xPeriod = 3;
        yPeriod = 2;
    }
    if (size === 12) {
        xPeriod = 4;
        yPeriod = 3;
    }
    sudokuStructure = [];
    sudokuRows = [];
    sudokuColumns = [];
    sudokuBlocks = [];
    sudokuDiagonals = [];
    allCells = [];
    allFields = [];
    const table = document.getElementById("sudoku");
    table.setAttribute("data-size", size);
    table.innerHTML = "";
    for(let i = 0; i<size; i++) {
        sudokuStructure[i] = [];
        sudokuRows[i] = new Field(size, "row"+(i+1));
        sudokuColumns[i] = new Field(size, "column"+(i+1));
        sudokuBlocks[i] = new Field(size, "block"+(i+1));
        allFields.push(sudokuRows[i]);
        allFields.push(sudokuColumns[i]);
        allFields.push(sudokuBlocks[i]);
    }
    if(gridDiagonals) {
        const diagonal1 = new Field(size, "diagonal1");
        const diagonal2 = new Field(size, "diagonal2");
        sudokuDiagonals.push(diagonal1);
        sudokuDiagonals.push(diagonal2);
        allFields.push(diagonal1);
        allFields.push(diagonal2);
    }

    for(let i = 0; i<size; i++) {
        const row = document.createElement("tr");
        for (let j = 0; j<size; j++) {
            const cell = document.createElement("td");
            cell.id = "cell_" + i + "_" + j;
            row.appendChild(cell);
            const cellObject = new Cell(
                size,
                cell
            )
            sudokuStructure[i][j] = cellObject;
            sudokuRows[i].addCell(cellObject);
            sudokuColumns[j].addCell(cellObject);
            sudokuBlocks[Math.floor(j/xPeriod)+yPeriod*Math.floor(i/yPeriod)]
                .addCell(cellObject);
            if (gridDiagonals) {
                if (i === j) {
                    sudokuDiagonals[0].addCell(cellObject);
                }
                if (size-i-1 === j) {
                    sudokuDiagonals[1].addCell(cellObject);
                }
            }
            allCells.push(cellObject);
        }
        table.appendChild(row);
    }
	
	for (let i=0; i<allFields.length; i++) {
		for (let j=i+1; j<allFields.length; j++) {
			var jointCells = [];
			for (const cell of allFields[i].cells) {
				if (allFields[j].cells.includes(cell)) jointCells.push(cell);
			}
			if (jointCells.length<2) continue;
			allFields[i].addOverlappingField(allFields[j],jointCells);
			allFields[j].addOverlappingField(allFields[i],jointCells);
        }
	}
    displayStatus("Created fresh and clean board");
}

initsudoku = function() {
    updateOptions();
    const buttons = document.getElementById("control");

    initPuzzle = new URLSearchParams(window.location.search).get('puzzle');
    if(initPuzzle) {
        readSudokuString(initPuzzle);
    } else {
        init(9);
    }

	for (ex in examples) {
		const bb = document.createElement("button");
		bb.innerHTML = "Example " + (parseInt(ex)+1);
		bb.setAttribute("onClick", "readSudokuString(examples["+ex+"])");
		buttons.appendChild(bb);
    }

    document.getElementById("solveOne").addEventListener("click", solveOne);
    document.getElementById("solveEasy").addEventListener("click", solveEasy);
    document.getElementById("solveAll").addEventListener("click", solveAll);
    document.getElementById("reset").addEventListener("click", restart);
    document.getElementById("clean").setAttribute("onClick", "init()");
    document.getElementById("export").addEventListener("click", getSudokuString);
    document.getElementById("click").addEventListener("click", updateOptions);
    document.getElementById("diagonals").addEventListener("click", updateDiagonals);
    document.getElementById("4x4").setAttribute("onClick", "init(4, true)");
    document.getElementById("6x6").setAttribute("onClick", "init(6, true)");
    document.getElementById("9x9").setAttribute("onClick", "init(9, true)");
    document.getElementById("12x12").setAttribute("onClick", "init(12, true)");
    document.getElementById("16x16").setAttribute("onClick", "init(16, true)");
}

window.addEventListener("load", initsudoku);

class Cell {
    constructor(size, htmlElement) {
        this.options = Cell.getAllAvailabeOptions(size);
        this.htmlElement = htmlElement;
        this.showOptions();
        this.fields = [];
    }

    addField(field) {
        this.fields.push(field);
    }

    static getAllAvailabeOptions(size) {
        return [...Array(size).keys()].map(x => x+1);
    }

    setValue(value, initial=false) {
        this.htmlElement.innerHTML = value;
        this.value = value;
        this.options = [];
		this.initial = initial;
        this.htmlElement.classList.add("done");
        this.htmlElement.classList.add("new");
        if (initial) this.htmlElement.classList.add("initial");
        this.fields.forEach(field => field.removeOption(value))
    }

    resetOptions(size) {
        if (!this.initial) {
			this.options = Cell.getAllAvailabeOptions(size);
			this.htmlElement.classList.remove("done");
			this.value = null;
			this.showOptions();
        }
    }

    resetValue() {
        if (this.initial) {
			this.setValue(this.value,true);
		}
    }

    optionClicked(option) {
        selectOptionOnClick
            ? this.selectOption(option)
            : this.removeOption(option);
    }

    selectOption(option) {
        this.setValue(option, selectAsInitial);
        if (solveAllWhenSelecting) solveAll();
    }

    removeOption(optionToRemove) {
        if (this.value) return;
        this.options = this.options.filter(option => optionToRemove !== option);
        this.showOptions();
    }

    setHint() {
        this.htmlElement.classList.add("hint");
    }

    setNew() {
        this.htmlElement.classList.add("new");
    }

    checkOne() {
        if (this.value) return false;
        if (this.options.length === 1) {
            const value = this.options[0];
            this.setValue(value);
            displayStatus("Only one possibility left: " + value + ".");
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
                this.optionClicked(option);
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
    constructor (size, name) {
        this.cells = [];
        this.name = name;
        this.size = size;
		this.overlappingFields = [];
    }

    addCell(cell) {
        this.cells.push(cell);
        cell.addField(this);
    }

	addOverlappingField(otherField,overlap) {
		this.overlappingFields.push([otherField,overlap]);
	}
	
    removeOption(option) {
        this.cells.forEach(cell => cell.removeOption(option))
    }

    checkDone() {
        if (this.done) return;
        this.done = true;
        for (const cell of this.cells) {
            if (!cell.value) this.done = false;
        }
    }

    checkLonelyNumbers() {
        if (this.done) return;
        for (const option of Cell.getAllAvailabeOptions(this.size)) {
            let count = 0;
            let theCell;
            for (const cell of this.cells) {
                if (cell.options.includes(option)) {
                    theCell=cell;
                    count++;
                }
            }
            if (count === 1 && !theCell.value) {
                displayStatus("Only one cell possible for " + option + ".");
                for (const cell of this.cells) cell.setHint();
                theCell.setValue(option);
                return true;
            }
        }
        return false;
    }

    checkBetweenOverlap() {
        if (this.done) return false;
		for (const other of this.overlappingFields) {
			if (this.checkBetween(...other)) return true;
		}
		return false;
	}
    checkBetween(otherField,jointCells) {
        var mySelectedCells = [];
        var otherSelectedCells = [];
        var jointSelectedCells = [];
        for (const option of Cell.getAllAvailabeOptions(this.size)) {
            mySelectedCells = [];
            for (const cell of this.cells) {
                if (cell.options.includes(option)) mySelectedCells.push(cell);
            }
            if (mySelectedCells.length === 0) continue;
            otherSelectedCells = [];
            for (const cell of otherField.cells) {
                if (cell.options.includes(option)) otherSelectedCells.push(cell);
            }
            if (otherSelectedCells.length === 0) continue;
            jointSelectedCells = [];
            for (const cell of jointCells) {
                if (cell.options.includes(option)) jointSelectedCells.push(cell);
            }
            if (otherSelectedCells.length === jointSelectedCells.length) {
                if (mySelectedCells.length === jointSelectedCells.length) continue;
                for (const cell of otherField.cells) {cell.setHint();}
                for (const cell of this.cells) {
                    cell.setHint();
                    if ((!jointCells.includes(cell)) && (cell.options.includes(option))) {
                        cell.removeOption(option);
                        cell.setNew();
                    }
                }
                displayStatus("Removing " + option + " outside the joint part of " + this.name + " and " + otherField.name + ".");
                return true;
            }
        }
        return false;
    }

    checkGroups() {
        if (this.done) return false;
        const unfinishedCells = [];
        for (const cell of this.cells) if (!cell.value) unfinishedCells.push(cell);
        if (unfinishedCells.length<2) return false;
        return this.collectGroups(unfinishedCells,[],0,1);
    }

    collectGroups(cellsToCheck, options, idx, depth) {
        for(let i = idx; i<cellsToCheck.length; i++) {
            const newOptions = [...options];
            for (const option of cellsToCheck[i].options) {
                if (!newOptions.includes(option)) newOptions.push(option);
            }
            if (newOptions.length > cellsToCheck.length-2) continue; // too many alternatives collected
            if (newOptions.length === depth) {
                // highlight and change outside elements
                var haveChanges=false;
                for (const cell of cellsToCheck) {
                    let cellHasOptionsInGroup = false;
                    let cellHasOptionsOutsideGroup = false;
                    for (const option of cell.options) {
                        if (newOptions.includes(option)) {
                            cellHasOptionsInGroup = true;
                        } else {
                            cellHasOptionsOutsideGroup = true;
                        }
                    }
                    if (cellHasOptionsInGroup && cellHasOptionsOutsideGroup) {
                        for (const option of cell.options) {
                            if (newOptions.includes(option)) {
                                cell.removeOption(option);
                            }
                        }
                        haveChanges = true;
                        cell.setNew();
                    }
                }
                if (haveChanges) {
                    cellsToCheck[i].setHint();
                    displayStatus("Delete " + newOptions + " outside the group.");
                }
                return haveChanges;
            }
            if (this.collectGroups(cellsToCheck,newOptions,i+1,depth+1)) {
                cellsToCheck[i].setHint();
                return true;
            }
        }
        return false;
    }
	
	findColours() {
		// find alternatives for this field
		if (this.done) return false;
		console.log("finding colours for " + this.name);
		const notSolvedCells = this.cells.filter(c => !c.value);
		let colours = [[]];
		for (const cell of notSolvedCells) {
			const tempColours = [];
			for (const colour of colours) {
				const unusedOptions = cell.options.filter(o => !colour.includes(o));
				for (const option of unusedOptions) {
					tempColours.push([...colour, option]);
				}
			}
			if (tempColours.length>16) return false;
			colours = tempColours;
		}
		console.log(colours);
		this.colours=colours;
		this.notSolvedCells=notSolvedCells;
	}

	alignColours(otherField) {
		if (this.done) return false;
		if (otherField.done) return false;
		const mediators = [];
		for (const mediator of this.overlappingFields) {
			if (mediator[0].done) continue;
			for (const m2 of otherField.overlappingFields) {
				if (mediator[0] == m2[0]) {
					if (mediator[1].filter(c => !c.value).length==0) break;
					if (m2[1].filter(c => !c.value).length==0) break;
					mediators.push([...mediator,m2[1]]);
					break;
				}
			}
		}
		if (mediators.length>0) console.log("try colouring " + this.name + " with " + otherField.name + " using " + mediators.map(m => m[0].name));
	}
}

function solve(stopAtDifficulty, keepGoing) {
    let done = true;
    for (const cell of allCells) {
        cell.dropTempClasses();
        if (!cell.value) done = false;
    }

    if (done) {
        victory();
        return;
    }

    for (const field of allFields) {
        field.checkDone();
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
        for (const field of allFields) {
            if (field.checkLonelyNumbers()) {
                foundSomething = true;
                break solveAttempts;
            }
        }

        difficultyReached = 3;
        for (const field1 of allFields) {
			if (field1.checkBetweenOverlap()) {
                foundSomething = true;
                break solveAttempts;
			}
        }

        difficultyReached = 4;
        for (const field of allFields) {
            if (field.checkGroups()) {
                foundSomething = true;
                break solveAttempts;
            }
        }

        difficultyReached = 5;
        for (const field of allFields) {
			field.findColours();
        }
		for (let i=0; i<allFields.length; i++) {
			for (let j=i+1; j<allFields.length; j++) {
				if (allFields[i].alignColours(allFields[j])) {
					foundSomething = true;
					break solveAttempts;
				}
			}
		}
        difficultyReached = 6;
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
    solve(3, true);
}

function solveAll() {
    solve(100, true);
}

function victory() {
    displayStatus("I did it!")
}

function restart() {
    for (const cell of allCells) {
        cell.dropTempClasses();
        cell.resetOptions(gridSize);
    }
    for (const cell of allCells) {
        cell.resetValue();
    }
    for (const field of allFields) {
        field.done = false;
    }
    displayStatus("Board has been reset.")
}