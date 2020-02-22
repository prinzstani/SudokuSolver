import Tkinter
from Tkconstants import *
import time
import os
from math import sqrt
from textwrap import fill

autoRunLevel=5
sampleFile = 'sudoku_sample.py'
solveFile = 'sudoku_solve.py'
standardFont='Terminal 6'
largeFont='Terminal 12'
fieldSize=35 # should adapt this to match different sudoku sizes
maxAuto=9

#sample
if os.path.isfile(sampleFile): execfile(sampleFile)
if os.path.isfile(solveFile): execfile(solveFile)

def newShow():
    global autoRunLevel
    autoRunLevel=(autoRunLevel+1)%(maxAuto+1)
    app.showbutton.configure(text='show ' + str(autoRunLevel))
    
class sudoku(Tkinter.Frame):
    def __init__(self,sample,master=None):
        Tkinter.Frame.__init__(self, master)
        self.groupSize=sample.size
        self.alternatives=sample.alternatives
        self.singleSizeX=sample.xsize
        self.singleSizeY=sample.ysize
        self.createSudokuStructure(sample)
        self.createSudokuGraphics()
        self.createButtons()
        self.setSample(sample)
        self.grid(row=0,column=0)
        self.announce('The sudoku solver')
        
    def announce(self,stri):
        self.master.title(stri)

    def createSudokuStructure(self,sample):
        self.frames=[[Tkinter.Frame(self,relief=RIDGE,borderwidth=2)
                      for idx1 in range(sample.xTotal/self.singleSizeX)]
                     for idx2 in range(sample.yTotal/self.singleSizeY)]
        self.fields= [[sudokuField(self.frames[idx2/self.singleSizeY][idx1/self.singleSizeX],idx2,idx1,fill(self.alternatives,max(self.singleSizeX,self.singleSizeY)))
                       for idx1 in range(sample.xTotal)]
                      for idx2 in range(sample.yTotal)]
        self.groups=[]
        for x,y in sample.parts:
            groupsHori=[sudokuGroup(self,[self.fields[j][i]
                                          for i in range(x,x+self.groupSize)])
                        for j in range(y,y+self.groupSize)]
            groupsVert=[sudokuGroup(self,[self.fields[j][i]
                                          for j in range(y,y+self.groupSize)])
                        for i in range(x,x+self.groupSize)]
            groupsBlock=[sudokuGroup(self,[self.fields[j+J][i+I]
                                           for j in range(self.singleSizeY)
                                           for i in range(self.singleSizeX)])
                         for J in range(y,y+self.groupSize,self.singleSizeY)
                         for I in range(x,x+self.groupSize,self.singleSizeX)]
            self.groups=self.groups+groupsHori+groupsVert+groupsBlock
        self.lastGroup=self.groups[0] # just an arbitrary one to start with
        for g in self.groups:
            g.ready=False

    def setSample(self, sample):
        self.clear()
        for idx in range(sample.xTotal):
            for idy in range(sample.yTotal):
                if sample.givenNumbers[idy][idx]<>' ':
                    self.fields[idy][idx]['text']=sample.givenNumbers[idy][idx]
                    self.fields[idy][idx].ready=True
                    self.fields[idy][idx]['font']=largeFont

    def createSudokuGraphics(self):
        for y, line in enumerate(self.fields):
            for x, item in enumerate(line):
                item.grid(row=y%self.singleSizeY, column=x%self.singleSizeX,
                          sticky='nesw')
        for y, line in enumerate(self.frames):
            for x, item in enumerate(line):
                item.grid(row=y, column=x, sticky='nesw')
                for row in range(self.singleSizeY):
                    item.grid_rowconfigure(row, minsize=fieldSize)
                for col in range(self.singleSizeX):
                    item.grid_columnconfigure(col, minsize=fieldSize)

    def makeButton(self, txt, posx, posy, conf):
        button=Tkinter.Button(self.buttonFrame,text=txt, background='grey')
        button.grid(row=posy,column=posx-1,sticky='nesw')
        button.configure(command=lambda config=conf: createSudoku(config))

    def clear(self):
        self.startbutton.config(background='grey')
        self.startbutton.config(command=self.renew)
        for g in self.groups:
            g.clear()

    def createButtons(self):
        self.buttonFrame=Tkinter.Frame(self.master,relief=RIDGE,borderwidth=2)
        self.startbutton=Tkinter.Button(self.buttonFrame,text='solve', background='grey')
        self.startbutton.grid(row=0,column=0,sticky='nesw')
        self.startbutton.configure(command=self.renew)
        self.quitbutton=Tkinter.Button(self.buttonFrame,text='quit', background='grey')
        self.quitbutton.grid(row=0,column=1,sticky='nesw')
        self.quitbutton.configure(command=self.quit)
        self.clearbutton=Tkinter.Button(self.buttonFrame,text='clear', background='grey')
        self.clearbutton.grid(row=0,column=2,sticky='nesw')
        self.clearbutton.configure(command=self.clear)
        self.showbutton=Tkinter.Button(self.buttonFrame,text='show '+str(autoRunLevel), background='grey')
        self.showbutton.grid(row=0,column=3,sticky='nesw')
        self.showbutton.configure(command=newShow)
#        self.makeButton('9x9',1,1,config0)
        self.makeButton('9x9: 1',1,1,config1)
        self.makeButton('9x9: 2',1,2,config2)
        self.makeButton('9x9: 3',1,3,config3)
        self.makeButton('9x9: 4',1,4,config4)
        self.makeButton('9x9: 5',1,5,config5)
        self.makeButton('9x9: 6',1,6,config6)
        self.makeButton('9x9: 7',1,7,config7)
        self.makeButton('9x9: 8',1,8,config31)
        self.makeButton('9x9: 9',1,9,config32)
        self.makeButton('9x9: 10',1,10,config33)

#        self.makeButton('16x16',2,1,config8)
        self.makeButton('16x16: 1',2,1,config25)
        self.makeButton('16x16: 2',2,2,config37)
        self.makeButton('16x16: 3',2,3,config38)
        self.makeButton('16x16: 4',2,4,config12)
        self.makeButton('16x16: 5',2,5,config11)
        self.makeButton('16x16: 6',2,6,config10)
        self.makeButton('16x16: 7',2,7,config9)
        self.makeButton('16x16: 8',2,8,config39)
        self.makeButton('16x16: 9',2,9,config40)
        self.makeButton('16x16: 10',2,10,config41)

        self.makeButton('multi: 1',3,1,config26)
        self.makeButton('multi: 2',3,2,config27)
        self.makeButton('multi: 3',3,3,config28)
        self.makeButton('multi: 4',3,4,config29)
        self.makeButton('multi: 5',3,5,config30)
        self.makeButton('multi: 6',3,6,config14)
        self.makeButton('multi: 7',3,7,config36)
        self.makeButton('multi: 8',3,8,config35)
        self.makeButton('multi: 9',3,9,config34)
        self.makeButton('multi: 10',3,10,config13)

        self.makeButton('6x6: 1',4,1,config15)
        self.makeButton('6x6: 2',4,2,config22)
        self.makeButton('8x8: 1',4,3,config16)
        self.makeButton('8x8: 2',4,4,config16)
        self.makeButton('10x10: 1',4,5,config17)
        self.makeButton('10x10: 2',4,6,config24)
        self.makeButton('12x12: 1',4,7,config18)
        self.makeButton('12x12: 2',4,8,config19)
        self.makeButton('15x15: 1',4,9,config20)
        self.makeButton('15x15: 2',4,10,config21)

        self.buttonFrame.grid(row=0,column=len(self.frames),sticky='nesw')
#        hvar=Tkinter.StringVar()
#        hvar.set("1")
#        hihi= Tkinter.OptionMenu(self.buttonFrame, hvar, "0", "1", "2", "3", command=self.report)
#        hihi.grid(row=2, column=1, sticky='nesw')
#        hoho=Tkinter.Button(self.buttonFrame,text="1",background='grey')
#        hoho.grid(row=3, column=1, sticky='nesw')
#        hoho.configure(command=lambda arg=3: self.selection(arg,self.groupSize+2))

    def selection(self,x,y):
        hvar=Tkinter.StringVar()
        hvar.set("1")
        self.hihi= Tkinter.OptionMenu(self, hvar, "0", "1", "5", "3",
                                 command=self.isSelected)
        self.hihi.grid(row=x, column=y, sticky='nesw')
        
    def isSelected(self,val):
        print 'the new selected value is ' + val
        self.hihi.destroy()
        
    def report(self,val):
        print 'the new value is ' + val

    def doNothing(self):
        self.announce("do not press the button while I am working")

    def renew(self):
        self.startbutton.config(background='grey')
        self.startbutton.config(command=self.doNothing)
        stepNumber=0
        level=0
        while level<10 and (autoRunLevel>level or stepNumber==0):
            self.lastGroup.activate(0)
            level=level+1
            for g in self.groups:
                if g.checkNew(level):
                    self.groups.remove(g)
                    self.groups.append(g)
                    self.lastGroup=g
                    if autoRunLevel>level:
                        self.update()
                        level=0
                        time.sleep(0.1)
                        break
                    else:
                        self.startbutton.config(background='green')
                        self.startbutton.config(command=self.renew)
                        return
        for g in self.groups:
            if not g.ready:
                self.announce('did not find anything')
                self.startbutton.config(background='red')
                self.startbutton.config(command=self.renew)
                return
        self.announce('Yeah, I got it')
        self.startbutton.config(background='green')
        self.startbutton.config(command=self.renew)

def createSudoku(conf):
    global app, root
    app.buttonFrame.destroy()
    app.destroy()
    app=sudoku(conf,master=root)

root=Tkinter.Tk()
app=sudoku(config7,master=root)
app.mainloop()
app.destroy()
root.destroy()
#Tkinter.sys.exit(0)
