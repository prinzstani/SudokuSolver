import Tkinter

def config1():
    global horizontal, vertical
    horizontal=[[4,2],[5],[1,2],[3,4,2,2],[3,6,4],[5,8,2,2],[2,2,9,1,1,1],
                [5,11,3,1],[18,1,2],[11,5,3],[8,8],[6,3,6],[1,1,3,3],[3,2,2],[4,3]]
    vertical=[[1],[4,2],[7],[1,6],[8],[9],[4,4,1],[1,4,1],[5,2],[6,1],[6,1],
              [7,1,2],[6,3],[1,6,2],[1,7,2],[1,6,2],[2,6,1],[1,1,5,1],[3,4],
              [2,3,3],[2,2,2,3],[1,2,2,2],[2,3],[2,3],[5]]

def config2():
    global horizontal, vertical
    horizontal=[[5,2],[5,5],[6,6],[6,7],[1,4,2,2],[2,7,3],[4,2,1,3,2],[4,3,2],
                [3,2,1,4],[10,2,3,5],[11,2,2,5],[4,1,1,5,3],[3,3,1,3,5],[5,4,7,2,2],
                [8,7,3,2],[6,1,2],[5,1,4],[4,2],[3,1,3],[6,1,3],[9,3],[15,3],
                [18,1],[3,1,18],[3,11,8],[11,6,5],[10,4,2,1],[10,1,3,2],[10,6],
                [8,4],[7,4],[5,1,1,3],[4,1,5],[11,4],[16,3],[18,2],[18],[18],
                [11,2,2],[7,1,2,1],[2,1,2,1,1],[3,2,3],[5,1,2,2],[6,2,2,2],[3,2,7],
                [3,3,3,5],[4,8,3,2],[3,3,7],[5,11,4,1],[2,3,9,7,2],[14,7],[5,2,3,5],
                [2,3,1,6,5],[4,4,9],[5,3,5]]
    vertical=[[1,1,1,3,1,1],[1,2,1,4,1,2],[1,2,2,7,2,1,1],[2,2,2,1,6,4,1],
              [1,2,2,1,11,2,2,1],[4,1,1,11,1,2,1],[4,1,18,3,1],[1,3,1,2,19,3,2],
              [3,3,2,2,8,14,2,3],[4,6,10,7,8,1,2],[8,5,6,2,9,9,2],[4,4,3,6,1,1,7,2,6],
              [4,4,12,1,7,1,2,7],[3,18,6,1,2,3,2],[4,15,7,1,10],[2,6,7,5,8],
              [2,4,7,5,6],[2,3,1,4,1,4,4,2],[2,5,5,7,4,2],[2,6,3,4,7,4,3],
              [3,2,1,5,3,4,1,2],[2,4,2,2,5,3,5,2,2],[2,3,2,2,1,5,8,2,3],
              [5,1,2,1,2,5,6,1,3,3],[5,2,1,2,1,2,3,2,5,1,6],[4,6,1,2,2,3,3,2,3,5],
              [4,3,1,2,3,3,2,1,3,4],[1,8,5,2,2,2],[6,6,5,3],[3,5,4,3]]

config2()
size_x = len(horizontal)
size_y = len(vertical)
optionLevel = 10
limit=1000
autoRun=True

def sumAll(li):
    if len(li)==1: return li[0]
    else: return li[0]+sumAll(li[1:])

sumHor=sumAll([sumAll(l) for l in horizontal])
sumVer=sumAll([sumAll(l) for l in vertical])
print 'horizontal sum = ' + str(sumHor)
print '  vertical sum = ' + str(sumVer)
if sumHor<>sumVer: exit

# Frame to hold the grid
f = Tkinter.Frame()

def getColor(x,y): return table[x][y]['background']
def setColor(c,x,y):
    table[x][0].prefer()
    table[0][y].prefer()
    if x<3 or size_x-x<3:
        for i in range(10): table[0][y].prefer()
    if y<3 or size_y-y<3:
        for i in range(10): table[x][0].prefer()
    if (c == 'black'): setBlack(x,y)
    else: setWhite(x,y)

def setWhite(x,y):
    table[x][y]['background']= 'white'
def setBlack(x,y):
    table[x][y]['background']='black'

def genVariants(l,li):
    if li == []: return [[True]*l]
    freeWhites = l-sumAll(li)+len(li)-1
    separator=[True]
    if len(li)==1:
        freeWhites=freeWhites+1
        separator=[]
    result=[]
    for cnt in range(0,freeWhites):
        result= result + \
            [ [True]*cnt+[False]*li[0]+separator+v
               for v in genVariants(l-cnt-li[0]-len(separator),li[1:]) ]
    return result

def genFittingVariants(l,li,line,limit,outer):
    if li == []:
        theResult=[True]*l
        if fitting(theResult,line): return [theResult]
        else: return []
    freeWhites = l-sumAll(li)+len(li)-1
    separator=[True]
    if len(li)==1:
        freeWhites=freeWhites+1
        separator=[]
    result=[]
    for cnt in range(0,freeWhites):
        startResult=[True]*cnt+[False]*li[0]+separator
        startLen=len(startResult)
        if fitting(startResult,line):
            recResult=genFittingVariants(l-startLen,li[1:],line[startLen:],limit,False)
            if recResult==0: return 0
            if recResult<>[]:
                result= result + [ startResult+v for v in recResult ]
                if len(result)>limit and not outer:
                    return 0
    return result

def mergeFittingVariants(l,li,line):
    if li == []:
        theResult=[True]*l
        if fitting(theResult,line): return theResult
        else: return 0
    freeWhites = l-sumAll(li)+len(li)-1
    separator=[True]
    if len(li)==1:
        freeWhites=freeWhites+1
        separator=[]
    result=0
    for cnt in range(0,freeWhites):
        startResult=[True]*cnt+[False]*li[0]+separator
        startLen=len(startResult)
        if fitting(startResult,line):
            recResult=mergeFittingVariants(l-startLen,li[1:],line[startLen:])
            if recResult<>0:
                locResult=startResult+recResult
                if result==0: result=locResult[:]
                else:
                    if not fitting(locResult,result):
                        for idx in range(len(result)):
                            result[idx] = mergeTwo(locResult[idx],result[idx])
                    if result==line: return result
    return result

def findOneChange(l,li,line):
    locLine=line[:]
    for idx in range(len(locLine)):
        if locLine[idx]=='grey':
            for poss in [True, False]:
                if checkOneVariant(l,li,locLine,idx,poss):
                    locLine[idx]=poss
                    return locLine
    return 0

def repres(el):
    if el==True: return '+'
    if el==False: return '-'
    return '?'
        
def checkOneVariant(l,li,line,idx,poss):
    if li == []:
        theResult=[True]*l
        if fitting(theResult,line): return poss==True
        else: return True
    freeWhites = l-sumAll(li)+len(li)-1
    separator=[True]
    if len(li)==1:
        freeWhites=freeWhites+1
        separator=[]
    for cnt in range(0,freeWhites):
        startResult=[True]*cnt+[False]*li[0]+separator
        startLen=len(startResult)
        if fitting(startResult,line):
            if idx < startLen:
                if possibleRest(l-startLen,li[1:],line[startLen:]):
                    if startResult[idx]<>poss:
#                        print 'problem with ' + str(poss) + ' at ' + str(idx)
                        return False
            else:
                if not checkOneVariant(l-startLen,li[1:],line[startLen:],
                                   idx-startLen,poss):
#                    print 'problem with ' + sumAll([repres(el) for el in line[startLen:]])
#                    print 'header is ' + sumAll([repres(el) for el in startResult])
                    return False
    return True

def possibleRest(l,li,line):
    if li == []:
        theResult=[True]*l
        return fitting(theResult,line)
    freeWhites = l-sumAll(li)+len(li)-1
    separator=[True]
    if len(li)==1:
        freeWhites=freeWhites+1
        separator=[]
    for cnt in range(0,freeWhites):
        startResult=[True]*cnt+[False]*li[0]+separator
        startLen=len(startResult)
        if fitting(startResult,line):
            if possibleRest(l-startLen,li[1:],line[startLen:]): return True
    return False

def mergeVariants(x):
    if x[0]==[]: return []
    theResult=x[0][:]
    for vari in x[1:]:
        if not fitting(vari,theResult):
            for idx in range(len(theResult)):
                theResult[idx] = mergeTwo(vari[idx],theResult[idx])
    return theResult

def fitting(line1,line2):
    for idx in range(0,len(line1)):
        if line1[idx]<>line2[idx] and line2[idx]<>'grey': return False
    return True

def mergeVariants(x):
    if x[0]==[]: return []
    theResult=x[0][:]
    for vari in x[1:]:
        if not fitting(vari,theResult):
            for idx in range(len(theResult)):
                theResult[idx] = mergeTwo(vari[idx],theResult[idx])
    return theResult

def mergeTwo(v1,v2):
    if v1==v2: return v1
    return 'grey'
    
def encode(c):
    if c=='grey': return c
    return c=='white'
def decode(c):
    if c=='grey': return c
    if c==True: return 'white'
    return 'black'

class controlLine(Tkinter.Button):
    listInts=[]
    freeCount=-1
    setCount=-1
    is_horizontal=True
    myPos=0
    ready=False
    preferred=1
    deferred=0
    myIter=[]
    myVariants=[]
    myLimit=limit
    def __init__(self,f,p,v,is_h):
        Tkinter.Button.__init__(self, f)
        self.listInts=v
        self.setCount=sumAll(v)
        self.is_horizontal=is_h
        self.myPos=p
        self.config(text=str(v))
        if (self.is_horizontal):
            self.myIter = [[x,self.myPos] for x in range(1,size_x+1)]
            self.config(text=sumAll([str(x)+' ' for x in v]))
        else:
            self.myIter = [[self.myPos,x] for x in range(1,size_y+1)]
            self.config(text=sumAll([str(x)+'\n' for x in v]))
        self.freeCount=len(self.myIter)-self.setCount

    def options(self):
        return self.countColor('grey') + self.setCount - \
               self.countColor('black')*3 + min(self.listInts) - \
               max(self.listInts)*4 + len(self.listInts)*4 + \
               self.deferred - self.preferred - self.listInts[0] - self.listInts[-1]
    def prefer(self):
        self.preferred=self.preferred+1
        self['background']='yellow'
    def unprefer(self):
        self.preferred=0
        self['background']='white'
    def countColor(self,c):
        cnt=0
        for it in self.myIter:
            if getColor(it[1],it[0])==c:
                cnt=cnt+1
        return cnt
    def extractColors(self):
        return [ encode(getColor(it[1],it[0])) for it in self.myIter ]
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
            if nl[idx] <> encode(getColor(it[1], it[0])):
                setColor(decode(nl[idx]),it[1],it[0])
    def checkVariants(self):
        global autoRun
        oldCount=len(self.myVariants)
        print 'handling line ' + str(self.myPos) + \
              ' (hori?: ' + str(self.is_horizontal) + ') ' + str(oldCount)
        line=self.extractColors()
        if oldCount==0:
            self.myVariants=genFittingVariants(len(line),self.listInts,line,self.myLimit,True)
            if self.myVariants==0: self.myVariants=[]
            print ' directly generated ' + str(len(self.myVariants))
        else:
            self.myVariants=[l for l in self.myVariants if fitting(l,line)]
        newCount=len(self.myVariants)
        print ' -> ' + str(newCount)
        if oldCount==newCount and newCount<>0:
            self.unprefer()
            return False
        if newCount<>0:
            newline=mergeVariants(self.myVariants)
            self.deferred=0
        else:
#            print 'merge the fitting variants'
#            newline=mergeFittingVariants(len(line),self.listInts,line)
#            newline=line
            self.deferred+=10
#            self.myLimit=self.myLimit*2
#            if line<>newline: print 'found changes'
            print 'find one change'
            nnnline=findOneChange(len(line),self.listInts,line)
            if nnnline==0:
                print 'not found a single change'
                nnnline=line
            else:
                print ' found a single change'
#            if nnnline<>newline: print 'more changes possible'
#            if not fitting(newline,nnnline):
#                print '******* incompatibility'
#                print 'newline = ' + sumAll([repres(el) for el in newline])
#                print 'nnnline = ' + sumAll([repres(el) for el in nnnline])
#                print '   line = ' + sumAll([repres(el) for el in line])
#                autoRun=False
#                return True
#            if not possibleRest(len(line),self.listInts,newline):
#                print 'newline is not correct'
#                autoRun=False
#                return True
            newline=nnnline
        if (line<>newline):
            self.newColors(newline)
            return True
        self.unprefer()
        return False

def hasgrey(li):
    for l in li:
        for el in l:
            if el=='grey': return True
    return False

def renew():
#    autoRun=True
    global optionLevel
    optionLevel-=5
    renewOne()
    while autoRun:
        optionLevel-=10
        renewOne()

def renewOne():
    global optionLevel, lastElement, autoRun
    lastElement['background']='white'
    table[0][0]['background']='black'
    veryAllHeads= \
        [table[0][i] for i in range(1,size_x+1) if not table[0][i].ready] + \
        [table[i][0] for i in range(1,size_y+1) if not table[i][0].ready]
    if veryAllHeads==[]:
        print('YES, I did it!!!')
        autoRun=False
        return
    allHeads= [el for el in veryAllHeads
               if el.options() < optionLevel and el.preferred>0]
    for el in veryAllHeads:
        if el.countColor('black')==el.setCount and not el.ready: 
            el.fill('white')
            lastElement=table[0][0]
            table[0][0]['background']='green'
            return
    for el in allHeads:
        if el.checkVariants():
            lastElement=el
            el['background']='orange'
            table[0][0]['background']='green'
            return
    if optionLevel<max(size_x,size_y)+100:
        optionLevel = optionLevel+1
        print("going up one step to level " + str(optionLevel))
        renewOne()
        return
    print 'Warning: did not find something new'
    autoRun=False

h_head = [controlLine(f,idx+1,horizontal[idx],False) for idx in range(len(horizontal))]
def h_bod():
    return [Tkinter.Button(f, text='', background='grey', foreground='orange', relief='raised') for cnt in horizontal]

table= \
 [[Tkinter.Button(f, text='', background='green', relief='raised')] + h_head] \
 + [[controlLine(f,idx+1,vertical[idx],True)] + h_bod() for idx in range(len(vertical))]
table[0][0].config(command=renew)
lastElement=table[0][0]

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

def switchColor(y,x,l):
  table[x][0].setReady(False)
  table[0][y].setReady(False)
  if getColor(x,y) == 'white': setBlack(x,y)
  elif getColor(x,y) == 'black': l.config(background = 'grey')
  else: setWhite(x,y)

# make all cells in the grid square
# iterating over the number of lines (rows)
for y in range(size_y+1):
    # make all rows the same height
    f.grid_rowconfigure(y, minsize=20)
for x in range(size_x+1):
    # make the columns the same size
    f.grid_columnconfigure(x, minsize=20)

def runChina():
    # display the frame
    f.pack()
    # run the event loop
    f.tk.mainloop()

runChina()
