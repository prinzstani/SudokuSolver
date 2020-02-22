
const example1 = "6   7 4 1"+" 7   298 "+"     65  "+"73   9  4"+"  261  78"+"    8    "+" 4 96 7 3"+" 8  53 42"+" 5    8  ";
const example2 = "    3   4"+"16 57 2  "+" 3   1  8"+"  9      "+"78 3 4 95"+"      1  "+"9  6   4 "+"  3 59 27"+"8   1    ";
setExample1 = function () {
    init(9);
    parseExample(example1, 9);
}

setExample2 = function () {
    init(9);
    parseExample(example2, 9);
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

window.addEventListener("load", () => init(9));

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