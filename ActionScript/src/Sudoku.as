package {
	import flash.display.Sprite;
	import flash.events.MouseEvent;
	import flash.text.TextField;
	import flash.utils.setTimeout;
//	import flash.ui.ContextMenu;
//	import flash.ui.ContextMenuBuiltInItems;
//	import flash.ui.ContextMenuItem;

	[SWF(backgroundColor=0xFFFFFF, width=600, height=420, frameRate=30)]

	public class Sudoku extends Sprite {
		private var myCells:Vector.<Cell> = new Vector.<Cell>();
		private var myRows:Vector.<Field> = new Vector.<Field>();
		private var myColumns:Vector.<Field> = new Vector.<Field>();
		private var myBlocks:Vector.<Field> = new Vector.<Field>();
		private var myFields:Vector.<Field> = new Vector.<Field>();
		private const waitTime:int = 150;
		private var OK:Boolean=false;
		private var doAll:int=0;
		public static var notice:TextField = new TextField();
		
//		private var myContextMenu:ContextMenu;
		public var background:Sprite;
		
		public function Sudoku() {
			var i:int; var j:int;
			var newCell: Cell;
			var f:Field;
			background = new Sprite();
			background.graphics.beginFill(0x555555,1);
			background.graphics.drawRect(0,0,600,420);
			background.graphics.endFill();
			addChild(background);
			for(i = 0; i<9; i++) {
				myRows.push(f=new Field("row"+(i+1))); myFields.push(f);
				myColumns.push(f=new Field("column"+(i+1))); myFields.push(f);
				myBlocks.push(f=new Field("block"+(i+1))); myFields.push(f);
			}
			for(i = 0; i<9; i++) {
				for(j = 0; j<9; j++) {
					newCell= new Cell(i,j);
					myCells.push(newCell);
					myRows[i].myCells.push(newCell);
					myColumns[j].myCells.push(newCell);
					myBlocks[Math.floor(j/3)+3*Math.floor(i/3)].myCells.push(newCell);
					addChild(newCell);
				}
			}
			createMenuItem(0,"solve one",solveOne);
			createMenuItem(1,"solve easy",solveEasy);
			createMenuItem(2,"solve all",solveAll);
			createMenuItem(3,"reset",reset);
			createMenuItem(10,"example 1",example);
			createMenuItem(11,"example 2",example);
			createMenuItem(12,"example 3",example);
			createMenuItem(13,"example 4",example);
			createMenuItem(14,"example 5",example);
			createMenuItem(15,"example 6",example);
			createMenuItem(16,"example 7",example);
			notice.x = 18;
			notice.y = 390;
			notice.width = 364;
			notice.height = 18;
			notice.background = true; 
			notice.border = true;
			addChild(notice);
		}
		
		private function solveOne(event:MouseEvent):void {
			doAll=0;
			realsolve();
		}

		private function solveEasy(event:MouseEvent):void {
			doAll=2;
			realsolve();
		}
		
		private function solveAll(event:MouseEvent):void {
			doAll=100;
			realsolve();
		}
		
		private function realsolve():void {
			//TODO: deactivate all cells
			for each (var c:Cell in myCells) {
				c.options();
			}
			OK=true;
			for each (var f:Field in myFields) {
				while (f.checkDeleteOne()) {}
				if (!f.checkOK()) OK=false;
			}
			for each (c in myCells) {
				if (c.checkOne()) {
					if (doAll>0) setTimeout(realsolve,waitTime);
					return;
				}
			}
			for each (f in myFields) {
				if (f.checkLonelyNumbers()) {
					if(doAll>1) setTimeout(realsolve,waitTime);
					return;
				}
			}
			for each (var f1:Field in myFields) {
				for each (var f2:Field in myFields) {
					if (f1.checkBetween(f2)) {
						if (doAll>2) setTimeout(realsolve,waitTime);
						return;
					}
				}
			}
			for each (f in myFields) {
				if (f.checkGroups()) {
					if (doAll>3) setTimeout(realsolve,waitTime);
					return;
				} 
			}
			if (OK) {
				notice.text = "Yes, I did it!";
				notice.backgroundColor = Cell.green;
			} else {
				notice.text = "Oops, something is wrong.";
				notice.backgroundColor = Cell.red;
			}
		}
		
		private function reset(event:MouseEvent):void {
			for each (var c:Cell in myCells) c.reset();
			for each (var f:Field in myFields) f.reset();
			notice.text = "";
			notice.backgroundColor = Cell.white;
		}

		private var examples:Array = new Array(
			"6   7 4 1"+" 7   298 "+"     65  "+"73   9  4"+"  261  78"+"    8    "+" 4 96 7 3"+" 8  53 42"+" 5    8  ",
			"    3   4"+"16 57 2  "+" 3   1  8"+"  9      "+"78 3 4 95"+"      1  "+"9  6   4 "+"  3 59 27"+"8   1    ",
			" 628   3 "+"  5  7  8"+"  4 9   6"+"4    9   "+"  7   5  "+"   2    1"+"8   5 7  "+"5  9  1  "+" 2   465 ",
			"4      9 "+"18  5 3  "+"  3   2  "+"   73  1 "+"94   8   "+"7     9  "+" 7   6   "+"  6   7 5"+"8   4    ",
			"  9  7 8 "+"83       "+" 1 6    7"+"    48  1"+"  6 3 8  "+"9  15    "+"2    1 6 "+"       54"+" 6 3  7  ",
			" 2   1   "+" 5 8   1 "+"   4 23  "+"4    7298"+"5       1"+" 39   4  "+"  3 45 6 "+"         "+"  8 6    ",
			"  2 4    "+" 5  7  3 "+"4 3  6  8"+"     95 1"+" 4  8  7 "+"1 67     "+"5  8  2 6"+" 6  3  5 "+"    2 8  "
			);
		
		private function example(event:MouseEvent):void {
			reset(event);
			var theExampleNumber:int = int(TextField(event.target).text.split(" ")[1]);
			var theExample:String=examples[theExampleNumber-1];
			for (var i:int=0; i<9; i++) {
				for (var j:int=0; j<9; j++) {
					setValue(i+1,j+1,int(theExample.charAt(i*9+j)));
				}
			}
		}
		
		private function setValue(x:int, y:int, val:int): void {
			if(val==0) return;
			myCells[9*(x-1)+y-1].setValue(val.toString());
		}
		
		private function createMenuItem(index:int, text:String, action:Function):void {
			var button:TextField = new TextField();
			button.x = 400/*+int(index/10)*100*/;
			button.y = 20+(index/*%10*/)*22;
			button.width = 80;
			button.height = 18;
			button.text = text;
			button.background = true; 
			button.border = true;
			button.addEventListener(MouseEvent.MOUSE_DOWN,action);
			addChild(button);
		}

		private function createLabel():TextField {
			var txtField:TextField = new TextField();
			txtField.text = "Right Click Here";
			return txtField;
		}

		private var myTextBox2:TextField = new TextField();
	}
}