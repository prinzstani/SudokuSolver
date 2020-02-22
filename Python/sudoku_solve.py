def setVarAndExit(top,i,posx,posy,f):
    if i=='*':
        f.fields[posx][posy].clear()
    else:
        f.fields[posx][posy]['text']=i
        f.fields[posx][posy].ready=True
        f.fields[posx][posy]['font']=largeFont
    top.destroy()

def reduceVarAndExit(top,i,posx,posy,f):    
    histr=list(f.fields[posx][posy]['text'])
    histr.remove(i[1])
    strihi=''
    for el in histr: strihi=strihi+el
    f.fields[posx][posy]['text']=strihi.strip()
    top.destroy()

def askNumber(posx,posy,f):
    top=Tkinter.Toplevel()
    top.title("Choose number")
    frame=Tkinter.Frame(top)
    frame.pack(expand=1,fill=BOTH)
    for i in range(len(f.alternatives)+1):
        if i==0: tt='*'
        else: tt=f.alternatives[i-1]
        button=Tkinter.Button(frame,text=tt,
                              command=lambda top=top,val=tt,posx=posx,posy=posy,f=f:
                              setVarAndExit(top,val,posx,posy,f))
        button.grid(row=0,column=i)
    for i in range(len(f.alternatives)):
        tt= '-' + f.alternatives[i]
        button=Tkinter.Button(frame,text=tt,
                              command=lambda top=top,val=tt,posx=posx,posy=posy,f=f:
                              reduceVarAndExit(top,val,posx,posy,f))
        button.grid(row=0,column=i+len(f.alternatives)+1)
    frame.mainloop()

class sudokuField(Tkinter.Button):
    ready=False
    def __init__(self,f,x,y,emptyText):
        Tkinter.Button.__init__(self, f, text='',
                                background='white', relief='raised',
                                font=standardFont,
                                command=lambda x=x,y=y,f=f: askNumber(x,y,f.master))
        self.emptyText=emptyText
    def activate(self,b):
        if b==2: self['background']='yellow'
        elif b==1: self['background']='green'
        else: self['background']='white'

    def clear(self):
        self['text']=self.emptyText
        self['font']=standardFont
        self.ready=False

# find all possible combinations of length pos
# of the numbers 0..maxy-1
def mergeNumbers(pos,maxy):
    global result
    result=[]
    collectedResult=[]
    while nextVariant(pos,maxy):
        collectedResult=collectedResult+[result[:]]
    return collectedResult

# auxiliary function for mergenumbers
def nextVariant(pos,maxi):
    global result
    if result==[]:
        result=range(pos)
        return maxi>pos
    else:
        for posi in range(pos-1,-1,-1):
            if result[posi]<maxi+posi-pos:
                result[posi]=result[posi]+1
                for pp in range(posi+1,pos):
                    result[pp]=result[posi]+pp-posi
                return True
        return False
        
class sudokuGroup:
    myFields=[]
    ready=False
    def __init__(self,master,fields):
        self.myFields=fields
        self.master=master
    def activate(self,b):
        for f in self.myFields: f.activate(b)
    def clear(self):
        for f in self.myFields: f.clear()
        self.ready=False
    def checkNew(self,level):
        if self.ready: return False
        if level == 1: return self.checkSelf()
        if level == 2: return self.checkDeleteOne()
        if level == 3: return self.checkOne()
        if level == 4: return self.checkLonelyNumbers()
        if level == 5: return self.checkBetween()
        if level < 15: return self.checkGroups(level-4)
        return False
    def checkSelf(self):
        for f in self.myFields:
            if not f.ready: return False
        self.ready=True
        self.activate(2)
        self.master.announce('whole group completed')
        return True
    def checkOne(self):
        for f in self.myFields:
            if not f.ready and len(f['text'])==1:
                f.activate(2)
                f.ready=True
                f['font']=largeFont
                self.master.announce('only one possibility left')
                return True
        return False
    def checkDeleteOne(self):
        for f in self.myFields:
            if f.ready:
                changeable=[f1 for f1 in self.myFields
                            if f1<>f and f['text'] in f1['text']]
                if changeable<>[]:
                    f.activate(1)
                    for f1 in changeable:
                        f1.activate(2)
                        histr=list(f1['text'])
                        histr.remove(f['text'])
                        strihi=''
                        for el in histr: strihi=strihi+el
                        f1['text']=strihi.strip()
                    self.master.announce('delete ' + f['text'] + ' from the other fields')
                    return True
        return False
    def checkLonelyNumbers(self):
        for n in range(len(self.master.alternatives)):
            possibleFields=[g1 for g1 in self.myFields
                            if self.master.alternatives[n] in g1['text']]
            f=possibleFields[0]
            if len(possibleFields) == 1 and not f.ready:
                f.activate(2)
                f['text']=self.master.alternatives[n]
                f.ready=True
                f['font']=largeFont
                self.master.announce('the only place for a ' + self.master.alternatives[n])
                return True
        return False
    def checkBetween(self):
        for otherGroup in self.master.groups:
            jointFields = [g1 for g1 in self.myFields
                             if g1 in otherGroup.myFields]
            if len(jointFields) > 1:
                for elem in self.master.alternatives:
                    myElems = [g1 for g1 in self.myFields
                               if elem in g1['text']]
                    if len(myElems) == 1: continue
                    otherElems = [g1 for g1 in otherGroup.myFields
                                  if elem in g1['text']]
                    if len(otherElems) == 1: continue
                    jointElems = [g1 for g1 in jointFields
                                  if elem in g1['text']]
                    if len(jointElems) == len(otherElems):
                        if len(jointElems) == len(myElems): continue
                        for jF in jointFields:
                            if elem in jF['text']:
                                jF.activate(1)
                        for mF in myElems:
                            if not mF in jointFields:
                                if elem in mF['text']:
                                    histr=list(mF['text'])
                                    histr.remove(elem)
                                    strihi=''
                                    for el in histr: strihi=strihi+el
                                    mF['text']=strihi.strip()
                                    mF.activate(2);
                        self.master.announce('delete ' + elem + ' outside the joint part')
                        return True;
        return False;
    def checkGroups(self,l):
        unknowns=[f for f in self.myFields if not f.ready]
        if l > len(unknowns)-2 or l < 2: return False
        for grp in mergeNumbers(l,len(unknowns)):
            cFields=[unknowns[idx]['text'] for idx in grp]
            elems = [c for c in self.master.alternatives if True in [c in x for x in cFields]]
            if len(elems) == l:
                found=False
                for idx in [e for e in range(len(unknowns)) if e not in grp]:
                    histr=list(unknowns[idx]['text'])
                    for c in elems:
                        if c in histr:
                            found=True
                            unknowns[idx].activate(2)
                            histr.remove(c)
                    strihi=''
                    for el in histr: strihi=strihi+el
                    unknowns[idx]['text']=strihi.strip()
                if found:
                    for idx in grp: unknowns[idx].activate(1)
                    self.master.announce('delete ' + str(elems) + ' outside the group')
                    return True
        return False
