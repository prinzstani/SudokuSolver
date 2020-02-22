package {
	public class Field {
		public var myCells:Vector.<Cell> = new Vector.<Cell>();
		public var OK:Boolean = false;
		public var name:String;

		public function Field(n:String) {
			name = n;
		}
		
		public function reset():void {
			OK=false;
		}
		
		public function checkOK():Boolean {
			if (OK) return true;
			for each (var c1:Cell in myCells) {
				if(!c1.OK) return false;
			}
			OK=true;
			return true;
		}
		
		public function checkDeleteOne():Boolean {
			if (OK) return false;
			for each (var c1:Cell in myCells) {
				if(c1.OK)
					for each (var c2:Cell in myCells) {
						if(c1!=c2 && c2.text.indexOf(c1.text)>=0) {
							c2.text=c2.text.replace(c1.text,"");
							return true;
						}
					}
			}
			return false;
		}

		public function checkLonelyNumbers():Boolean {
			var theCell:Cell;
			var count:int;
			if (OK) return false;
			for each (var option:String in Cell.allOptions.split("")) {
				count=0;
				for each (var c:Cell in myCells) {
					if (c.text.indexOf(option) >=0) {
						theCell=c;
						count++;
					}
				}
				if (count == 1 && ! theCell.OK) {
					Sudoku.notice.text="only one cell possible for " + option;
					for each (c in myCells) c.highlight(false);
					theCell.highlight(true);
					theCell.setValue(option);
					return true;
				}
			}
			return false;
		}
		
		public function checkBetween(otherField:Field):Boolean {
			if (OK) return false;
			if (otherField == this) return false;
			var jointCells:Vector.<Cell> = new Vector.<Cell>();
			var mySelectedCells:Vector.<Cell> = new Vector.<Cell>();
			var otherSelectedCells:Vector.<Cell> = new Vector.<Cell>();
			var jointSelectedCells:Vector.<Cell> = new Vector.<Cell>();
			for each (var c:Cell in otherField.myCells) if (myCells.indexOf(c) >=0) jointCells.push(c);
			if (jointCells.length<2) return false;
			for each (var option:String in Cell.allOptions.split("")) {
				mySelectedCells = new Vector.<Cell>();
				for each (c in myCells) if (c.text.indexOf(option) >=0) mySelectedCells.push(c);
				if (mySelectedCells.length == 1) continue; 
				otherSelectedCells = new Vector.<Cell>();
				for each (c in otherField.myCells) if (c.text.indexOf(option) >=0) otherSelectedCells.push(c);
				if (otherSelectedCells.length == 1) continue; 
				jointSelectedCells = new Vector.<Cell>();
				for each (c in jointCells) if (c.text.indexOf(option) >=0) jointSelectedCells.push(c);
				if (otherSelectedCells.length == jointSelectedCells.length) {
					if (mySelectedCells.length == jointSelectedCells.length) continue;
					for each (c in otherField.myCells) c.highlight(false);
					for each (c in myCells) {
						c.highlight(false);
						if ((jointCells.indexOf(c)<0) && (c.text.indexOf(option)>=0)) {
							c.text=c.text.replace(option,"");
							c.highlight(true);
						}
					}
					Sudoku.notice.text="removing " + option + " outside the joint part of " + name + " and " + otherField.name;
					return true;
				}
			}
			return false;
		}
		
		public function checkGroups():Boolean {
			if (OK) return false;
			var unfinishedCells:Vector.<Cell> = new Vector.<Cell>();
			for each (var c:Cell in myCells) if (!c.OK) unfinishedCells.push(c);
			if (unfinishedCells.length<2) return false;
			return collectGroups(unfinishedCells,"",0,1);
		}
		
		public function collectGroups(cells:Vector.<Cell>, options:String, idx:Number, depth:Number):Boolean {
			for(var i:Number = idx; i<cells.length; i++) {
				var newOptions:String = options;
				for each (var opt:String in cells[idx].text.split("")) {
					if (newOptions.indexOf(opt) < 0) newOptions+=opt;
				}
				if (newOptions.length > cells.length-2) return false; // too many alternatives collected
				if (newOptions.length == depth) {
					Sudoku.notice.text="delete " + newOptions + " outside the group";
					cells[idx].highlight(false);
					// highlight and change outside elements
					var haveChanges:Boolean=false;
					for each (var c:Cell in cells) {
						var newText:String = c.text;
						var changed:Boolean = false;
						for each (opt in newOptions.split("")) {
							if (newText.indexOf(opt) >= 0) {
								newText=newText.replace(opt,"");
								changed = true;
							}
						}
						if (changed && newText.length>0) {
							c.text = newText;
							haveChanges = true;
							c.highlight(true);
						}
					}
					return haveChanges;
				}
				if (collectGroups(cells,newOptions,i+1,depth+1)) {
					cells[idx].highlight(false);
					return true;
				}
			}
			return false;
		}
	}
}