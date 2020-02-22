import Tkinter

#config 1
horizontal=[0,18,0,16,2,5,5,11,5,5,3,8,0]
vertical=[0,1,8,1,9,2,4,4,2,4,4,3,2,8,2,7,1,4,2,1,9,0]
sizesToFill=[7,7,7,7,7,7,6,6,5,4,4,4,3,2,1,1]
whites=[[9,2],[10,2],[11,2],[11,3],[9,4],[10,4],[11,4],[6,18],[6,20],[7,20],[8,20],[8,21]]
blacks=[[10,3],[7,21]]

size_x = len(horizontal)
size_y = len(vertical)

# Frame to hold the grid
f = Tkinter.Frame()

def getColor(x,y): return table[x][y]['background']
def setColor(c,x,y):
    if (c == 'black'): setBlack(x,y)
    else: setWhite(x,y)

def setWhite(x,y):
    if getColor(x,y)!='white':
        table[x][y]['background']= 'white'
        if x>0:
            if getColor(x-1,y)=='black': setBlack(x-1,y)
        if y>0:
            if getColor(x,y-1)=='black': setBlack(x,y-1)
        if x+1<size_y:
            if getColor(x+1,y)=='black': setBlack(x+1,y)
        if y+1<size_x:
            if getColor(x,y+1)=='black': setBlack(x,y+1)
def setBlack(x,y):
    table[x][y]['background']='black'
    setWhite(x+1, y+1)
    setWhite(x+1, y-1)
    setWhite(x-1, y+1)
    setWhite(x-1, y-1)
    x1=x2=x
    while getColor(x1,y)=='black': x1=x1-1
    while getColor(x2,y)=='black': x2=x2+1
    if (getColor(x1,y) == 'white' and getColor(x2,y) == 'white'):
        x1=x1+1
        x2=x2-1
        if (x1<>x2):
            for xh in range(x1,x2+1):
                table[xh][y]['text']= 'o'
            boatFound(x2-x1+1)
    y1=y2=y
    while getColor(x,y1)=='black': y1=y1-1
    while getColor(x,y2)=='black': y2=y2+1
    if (getColor(x,y1) == 'white' and getColor(x,y2) == 'white'):
        y1=y1+1
        y2=y2-1
        if (y1<>y2):    
            for yh in range(y1,y2+1):
                table[x][yh]['text']= 'o'
            boatFound(y2-y1+1)
    if (x1 == x2 and y1 == y2):
        table[x1][y1]['text']= 'o'
        boatFound(1)

def boatFound(n):
    if n in sizesToFill:
        z1=sizesToFill.index(n)
        sizesToFill[z1]=0
        for b in boats[z1]:
            b['background'] = 'orange'
    else:
        print 'Warning: Boat of size ' + str(n) + ' not requested!'

def genVariants(x,bs,ws):
    if x == []: return [[]]
    h=x[0]
    t=[ l for l in genVariants(x[1:],bs,ws) \
        if l.count('black')<=bs and l.count('white') <= ws ]
    if h=='grey':
        return [ [hh]+el for el in t for hh in ['black','white']]
    else: return [ [h]+el for el in t ]

def validLine(line,bs,listi,ori):
    if bs != line.count('black'): return False
    hi= allBoats(line)
    ha= allBoats(ori)
    for b in listi:
        if not b in hi: return False
    for l in range(2,max(hi)+1):
        if hi.count(l) - ha.count(l) > sizesToFill.count(l): return False
    return True

def mergeVariants(x):
    if x[0]==[]: return []
    return [mergeOne(set([el[0] for el in x]))] + mergeVariants([el[1:] for el in x])
def mergeOne(s):
    if len(s)==1: return s.pop()
    else: return 'grey'

def allBoats(line):
    idx=0
    result=[]
    while True:
        while idx < len(line) and line[idx]=='white': idx=idx+1
        if idx == len(line): return result
        startidx=idx
        while line[idx]=='black': idx=idx+1
        if line[idx]=='white': result.append(idx-startidx)
        while line[idx]!='white': idx=idx+1

class controlLine(Tkinter.Button):
    listInts=[]
    freeCount=-1
    setCount=-1
    is_horizontal=True
    myPos=0
    ready=False
    myIter=[]
    myVariants=[]
    def __init__(self,f,p,v,is_h):
        Tkinter.Button.__init__(self, f)
        if (type(v)==list): self.listInts=v
        else: self.setCount=v
        self.is_horizontal=is_h
        self.myPos=p
        self.config(text=str(v))
        if (self.is_horizontal):
            self.myIter = [[x,self.myPos] for x in range(1,size_x+1)]
        else:
            self.myIter = [[self.myPos,x] for x in range(1,size_y+1)]
        self.freeCount=len(self.myIter)-self.setCount
    def countcolor(self,c):
        cnt=0
        for it in self.myIter:
            if getColor(it[1],it[0])==c:
                cnt=cnt+1
        return cnt
    def extractColors(self):
        return [ getColor(it[1],it[0]) for it in self.myIter ]
    def fill(self,c):
        for it in self.myIter:
            if getColor(it[1],it[0])=='grey':
                setColor(c,it[1],it[0])
        self.setReady(True)
    def setReady(self,b):
        self.ready=b
        if b: self.config(background='green')
        else: self.config(background='white')
    def newColors(self,nl):
        for idx in range(len(nl)):
            it=self.myIter[idx]
            if nl[idx] <> getColor(it[1], it[0]):
                setColor(nl[idx],it[1],it[0])

def checkVariants(el):
    print 'handling line ' + str(el.myPos) + ' (hori?: ' + str(el.is_horizontal) + ')'
    line=el.extractColors()
    variants=genVariants(line,el.setCount,el.freeCount)
    print 'found some variants: ' + str(len(variants))
    goodVariants=[l for l in variants if validLine(l, el.setCount, el.listInts, line)]
    el.myVariants=[allBoats(l) for l in goodVariants]
    print 'found good variants: ' + str(len(goodVariants))
    newline=mergeVariants(goodVariants)
    if (line<>newline):
        el.newColors(newline)
        return True
    return False
    
def renew():
    all_heads= \
        [table[0][i] for i in range(1,size_x+1) if not table[0][i].ready] + \
        [table[i][0] for i in range(1,size_y+1) if not table[i][0].ready]
    for el in all_heads:
        if el.countcolor('black')==el.setCount and not el.ready: 
            el.fill('white')
            return
    for el in all_heads:
        if el.countcolor('black')+el.countcolor('grey')==el.setCount and not el.ready:
            el.fill('black')
            return
    for el in all_heads:
        if checkVariants(el): return
    for s in sizesToFill:
        if s > 1:
            possibleHeads=[el for el in all_heads if
                           [a for a in el.myVariants if s in a] <> []]
            print 'possibleHeads for ' + str(s) + ' are ' + str(len(possibleHeads))
            if len(possibleHeads)==1:
                chosenOne=possibleHeads[0]
                if not s in chosenOne.listInts:
                    chosenOne.listInts = chosenOne.listInts + [s]
                    print 'have chosen ' + str(chosenOne.myPos) + ' (hori?: ' + str(chosenOne.is_horizontal) + ') with ' + str(s)
                    if checkVariants(chosenOne): return
    print 'Warning: did not find something new'

h_head = [controlLine(f,idx+1,horizontal[idx],False) for idx in range(len(horizontal))]
def h_bod():
    return [Tkinter.Button(f, text='', background='grey', foreground='orange', relief='raised') for cnt in horizontal]

table= \
 [[Tkinter.Button(f, text='', background='black', relief='raised')] + h_head] \
 + [[controlLine(f,idx+1,vertical[idx],True)] + h_bod() for idx in range(len(vertical))]
table[0][0].config(command=renew)

# Iterate over all lines (y axis),
# then per line over all items (x axis)
for y, line in enumerate(table):
    for x, item in enumerate(line):
        if isinstance(item,controlLine):
            item.config(background='white')
        elif x+y>0:
            item.config(command=lambda x=x, y=y, item=item: switchColor(x,y,item))
        # and place it into the grid, specifying that it should fill
        # the entire cell (north, east, south, west)
        item.grid(row=y, column=x, sticky='nesw')

for y, line in enumerate(whites):
  table[line[1]][line[0]]['background'] = 'white'
for y, line in enumerate(blacks):
  table[line[1]][line[0]]['background'] = 'black'

def switchColor(y,x,l):
  table[x][0].setReady(False)
  table[0][y].setReady(False)
  if getColor(x,y) == 'white': setBlack(x,y)
  elif getColor(x,y) == 'black': l.config(background = 'grey')
  else: setWhite(x,y)

# make all cells in the grid square
# iterating over the number of lines (rows)
for y in range(size_y):
    # make all rows the same height
    f.grid_rowconfigure(y, minsize=8)
for x in range(size_x):
    # make the columns the same size
    f.grid_columnconfigure(x, minsize=8)

boats=[]
if type(sizesToFill)==list and sizesToFill<>[]:
    for idx in range(len(sizesToFill)):
        boats.append([])
        f.grid_columnconfigure(size_x+2*idx+1, minsize=6)
        for el in range(sizesToFill[idx]):
            b=Tkinter.Button(f, text=str(sizesToFill[idx]), background='white', relief='raised')
            b.grid(row=1+el, column=size_x+2*idx+2, sticky='nesw')
            boats[idx].append(b)
    f.grid_columnconfigure(size_x+1, minsize=20)

# display the frame
f.pack()
# run the event loop
f.tk.mainloop()
