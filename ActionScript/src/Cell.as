package {
	import flash.events.TextEvent;
	import flash.text.TextField;
	import flash.text.TextFieldType;
	import flash.text.TextFormat;
	import flash.text.TextFormatAlign;

	public class Cell extends TextField {
		public static const white:uint  = 0xFFFFFF;
		public static const yellow:uint = 0xFFFF00;
		public static const orange:uint = 0xFF9900;
		public static const red:uint    = 0xD80505;
		public static const green:uint  = 0x1CA91B;
		//public static const blue:uint   = 0x0018EE;
		public static const blue:uint   = 0xCCFFFF;

		private var row:int, col:int;
		public var OK:Boolean = false;
		public static const allOptions:String = "123456789";

		public function Cell(c:int, r:int) {
			row=r; col=c;
			width = 40; height = 40;
			background = true; border = true;
			type = TextFieldType.INPUT;
			maxChars = 1; 
			var format:TextFormat = new TextFormat();
			format.size = 36;
			format.align = TextFormatAlign.CENTER;
			restrict=" 1-9";
			defaultTextFormat = format;
			x=18+40*row+2*Math.floor(row/3); y=18+40*col+2*Math.floor(col/3);
			addEventListener(TextEvent.TEXT_INPUT,textInputHandler);
		}
		
		public function highlight(strong:Boolean):void {
			if (strong) backgroundColor = yellow;
			else backgroundColor = blue;
		}

		public function reset():void {
			OK=false;
			text="";
			backgroundColor = white;
		}
		
		public function options():void {
			if (text.length<1) {
				var format:TextFormat = new TextFormat();
				format.size = 10;
				format.align = TextFormatAlign.CENTER;
				defaultTextFormat = format;
				text=allOptions;
			}
			if (OK && (text.length==1)) backgroundColor = green;
			else backgroundColor = white;
		}
		
		public function checkOne():Boolean {
			if (OK) return false;
			if (text.length==1) {
				setValue(text);
				Sudoku.notice.text="only one possibility left: " + text;
				return true;
			}
			return false;
		}
		
		public function setValue(val:String):void {
			var format:TextFormat = new TextFormat();
			format.size = 36;
			format.align = TextFormatAlign.CENTER;
			defaultTextFormat = format;
			text=val.toString();
			OK=true;
			highlight(true);
		}
		
		public function textInputHandler(event:TextEvent):void {
			highlight(true);
		}
	}
}