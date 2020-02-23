
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

parseExample = function (example, size) {
    for(let i = 0; i<size; i++) {
        for (let j = 0; j<size; j++) {
            const character = example.charAt(i*size+j)
            if (character != ' ') {
                sudokuStructure[i][j].setValue(character);
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
    const table = document.getElementById("sudoku");
    table.innerHTML = "";

    for(let i = 0; i<size; i++) {
        sudokuStructure[i] = [];
        const row = document.createElement("tr");
        for (let j = 0; j<size; j++) {
            const cell = document.createElement("td");
            cell.id = "cell_" + i + "_" + j;
            row.appendChild(cell);
            sudokuStructure[i][j] = new Cell(size, cell);
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
}

window.addEventListener("load", () => initsudoku());

class Cell {
    constructor(size, htmlElement) {
        this.options = [...Array(size).keys()].map(x => x+1);
        this.htmlElement = htmlElement;
    }

    setValue(value) {
        this.htmlElement.innerHTML = value;
        this.value = value;
        this.options = [];
    }
}
