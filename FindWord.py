from operator import itemgetter, attrgetter
import os
import itertools

#1, open index file and compose to a whole file.
#2, count all the situations.
plist = []
pdict={}
findword=0;
FoundKeyList = []
FoundValidWordList = []
FoundUnsortedWordList = []
FoundWordList = []

def ReadIndexFile():
    for root, sub_dirs, files in os.walk("D:\\AWD\\Words\\Original"):
        for fname in files:
            findex = open(root+"\\"+fname, "r")
            alllines = findex.readlines()
            for line in alllines:
                line=line.strip('\n')
                if line[0] == ' ':
                    continue
                line=line.split(' ')
                plist.append(line[0])
            del alllines
            findex.close()

def MakeMap():
    plist.sort()
    for word in plist:
        sortword = sorted(word)
        sortword="".join(sortword)
        if pdict.has_key(sortword):
            if word not in pdict[sortword]:
                pdict.setdefault(sortword,[]).append(word)
        else:
            pdict.setdefault(sortword,[]).append(word)
    fout = open("index.all","w")
    fout.write(str(pdict))
    fout.close()
   
def ReadMap():
    fin = open("index.all","r")
    pdict = eval(fin.read())
    fin.close()
    return pdict

def Cominations(sortedWord, number):
    global findword
    findword=0
    n = len(sortedWord)
    m = int(number)
    if m > n:
        m=n
    order = []
    for i in range(m+1):
        order.append(i-1)
    count=0
    k = m
    flag = True
    while order[0] == -1:
        if flag:
            oneword = []
            for i in range(1,m+1):
                oneword.append(sortedWord[order[i]])
            FindWord( oneword, count )
            count = count + 1
            flag = False
            
        order[k] = order[k]+1
        if order[k] == n:
            order[k] = 0
            k=k-1
            continue
        if k < m:         
            order[k+1] = order[k];
            k=k+1
            continue
    
        if k == m:
            flag = True
    del order

def FindWord(fword, count):
    global findword
    global FoundKeyList
    global FoundWordList

    FoundKeyList = []
    strPermut = "".join(fword);
    if pdict.has_key(strPermut) and strPermut not in FoundKeyList:
        FoundKeyList.append(strPermut)
        for w in pdict[strPermut]:
            if w not in FoundWordList:
                FoundWordList.append(w)
        findword = findword + 1
    del strPermut
        
def FindWord_All(rword, wlen):
    print("Find word in: " + rword + "  /Length is: " + wlen)
    sortrword = sorted(rword)
    Cominations( sortrword, wlen )
    
  
class Node(object):
    def __init__(self, data = -1, index = 0, parent = None):
        self.data = data
        self.index = index
        self.parent = parent
        if parent:
            self.level = parent.level + 1
        else:
            self.level = 0
        self.children = []


    def append(self, child):
        self.children.append(child)

class WordTree(object):
    def __init__(self):
        self.root = Node()
        
    def addRoot(self, data, index):
        node = Node(data, index)
        self.root = node
        return node
    
    def addChild(self, data, index, pNode):
        node = Node(data, index, pNode)
        tree_node = pNode
        while tree_node != None:
            if tree_node.index == index:
                return None
            tree_node = tree_node.parent
        pNode.children.append(pNode)
        return node
    
    def isEmpty(self):
        return True if self.root.data == -1 else False

w = 4
h = 4
maxWordLength=8
wt = WordTree()
lword = list("leanbgemearptaus")
def TraversalWord():
    global lword
    global maxWordLength
    lword = raw_input("Input all the characters: ")
    maxWordLength = int(raw_input("Input the MAX length: "))
    for index in range(16):
        #build tree
        c = lword[index]
        fout.write("-----" + c + "--" + str(index) + "\n")
        curNode = wt.addRoot(c, index)
        RecurTraverse(curNode, index)
 
childFactorX=(-1,-1,-1, 0, 1, 1, 1, 0)
childFactorY=(-1, 0, 1, 1, 1, 0,-1,-1)
count = 0
def RecurTraverse(node, index):
    global count
    global FoundKeyList
    global FoundValidWordList
    global FoundUnsortedWordList
    global fout
    global findword
    
    x = index%w
    y = index/h
    succ=0
    for i in range(8):
        cx = x + childFactorX[i]
        cy = y + childFactorY[i]
        cindex = cy*w + cx
        if cx < 0 or cy < 0 or cx >= w or cy >= h:
            continue
        cnode = wt.addChild(lword[cindex], cindex, node) 
        if cnode:
            succ = succ+1
            if cnode.level == maxWordLength-1:
                word=""
                pNode = cnode
                while pNode != None:
                    word = pNode.data + word
                    pNode = pNode.parent
                FoundUnsortedWordList.append(word)    
                word = sorted(word)
                strPermut = "".join(word);
                if pdict.has_key(strPermut) and strPermut not in FoundKeyList:
                    FoundKeyList.append(strPermut)
                    for wd in pdict[strPermut]:
                        FoundValidWordList.append(wd)
                    findword = findword + 1
                del strPermut

            elif cnode.level > maxWordLength-1:
                continue
            else:
                RecurTraverse(cnode, cindex)
        
    if succ==0:
        return None
    
#ReadIndexFile()
#MakeMap()

fout = open("d:\\log.txt","w")
pdict = ReadMap()

#===============================================================================
# while True:
#     sword = raw_input("Input unsorted characters: ")
#     wlen = raw_input("Input the MAX length: ")
#     FindWord_All( sword, wlen )
#     FoundWordList.sort()
#     for w0 in FoundWordList:
#         print w0
#===============================================================================

  
TraversalWord()
print "word found:"
FoundValidWordList.sort()

for w0 in FoundUnsortedWordList:
    if w0 in FoundValidWordList:
        if w0 not in FoundWordList:
            FoundWordList.append(w0)
for w0 in FoundWordList:
    print w0
  
foundWord = list(raw_input("Input the found word: "))
lword=list(lword)
for w0 in foundWord:
    lword.remove(w0)
  
lword="".join(lword)
print "Left characters: " + lword
  
for i in range(2):
    findWordLen = raw_input("Input another word length: ")
    FindWord_All(lword, findWordLen)
    for w0 in FoundWordList:
        print w0
  
print "All Done!"

