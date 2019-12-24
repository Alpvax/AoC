from .. import intcode
import os, collections

class Data:
    def __init__(self, result=None, liveDisplay=False):
        self.__data = {}
        self._liveDisplay = liveDisplay
        self.row = 0
        self.column = 0
        self.maxCol = 0
        self.rPos = None
        self.rDir = collections.deque("^>v<")
        self.intersections = {}
        self._instructions = {}
        self.lastInputRaw = None
        if result:
            for res in result:
                self.recieveResult(res)
    def recieveResult(self, result):
        self.lastInputRaw = result
        c = chr(result)
        if c == "\n":
            self.row += 1
            self.maxCol = max(self.column, self.maxCol)
            self.column = 0
        else:
            if c in "<^>v":
                self.rPos = (self.column, self.row)
            self.__data[(self.column,self.row)] = c
            self.column += 1
        if self._liveDisplay:
            print(c, end="")
    def display(self):
        for r in range(self.row - 1):
            for c in range(self.maxCol):
                print(self.__data.get((c, r)), end="")
            print()
    def updateIntersections(self):
        def isIntersection(pos):
            if self.__data.get(pos) != "#":
                return False
            for x, y in ((0,-1), (-1,0), (0,1), (1,0)):
                if self.__data.get((pos[0] + x, pos[1] + y)) != "#":
                    return False
            return True
        self.intersections = {pos: pos[0] * pos[1] for pos in self.__data if isIntersection(pos)}
        return sum(self.intersections.values())
    #def addInstruction(self, name, ilist):
    #    self._instructions[name] = ilist
    #def updateRobot(self, instruction):
    #    if instruction in self._instructions:
    #        for i in self._instructions[instruction]:
    #            self.updateRobot(i)
    #    else:
    #        if instruction == "L":
    #            self.rDir.rotate()
    #        elif instruction == "R":
    #            self.rDir.rotate(-1)
    #        else:
    #            self.__data[self.rPos] = "?"
    #            num = int(instruction)
    #            x = self.rPos[0]
    #            y = self.rPos[1]
    #            d = self.rDir[0]
    #            if d == "<":
    #                x -= num
    #            elif d == "^":
    #                y -= num
    #            elif d == ">":
    #                x += num
    #            elif d == "v":
    #                y += num
    #            self.rPos = (x, y)
    #    self.__data[self.rPos] = self.rDir[0]

data = Data(liveDisplay=False)

@intcode.IntCodeOperator(4)
def ASCIIOutputOp(a):
    data.recieveResult(a)

with open(os.path.dirname(__file__) + "/input.txt") as f:
  inputData = [int(n) for n in f.read().split(",")]

machine = intcode.IntCodeMachine(inputData)
machine.start()
#data = Data(machine._out)
print(data.updateIntersections())
#data = {}
#row = 0
#col = 0
#maxCol = 0
#for o in machine._out:
#    c = chr(o)
#    if c == "\n":
#        row += 1
#        maxCol = max(col, maxCol)
#        col = 0
#    else:
#        #print("{} = {}".format((col,row), c))
#        data[(col,row)] = c
#        col += 1
#
#def display():
#    for r in range(row - 1):
#        for c in range(maxCol):
#            print(data.get((c, r), " "), end="")
#        print()
#
#def isIntersection(pos):
#    for x, y in ((0,-1), (-1,0), (0,1), (1,0)):
#        if data.get((pos[0] + x, pos[1] + y), ".") != "#":
#            return False
#    return True
#
#intersections = {pos: pos[0] * pos[1] for pos,c in data.items() if c == "#" and isIntersection(pos)}
#
#for i in intersections:
#    data[i] = "O"
#print(sum(i for p,i in intersections.items()))

# L6L4R12L6R12R12L8L6L4R12L6L10L10L6L6R12R12L9L6L4R12L6L10L11L6L6R12R12L8L6L4R12L6L10L10L6
#A = L6L4R12
# => AL6R12R12L8AL6L10L10L6L6R12R12L9AL6L10L11L6L6R12R12L8AL6L10L10L6
#B = L6R12R12L6
# => ABL8AL6L10L10L6BL10AL6L10L10L6BL8AL6L10L10L6
#C = L6L10L10L6
# => ABL8ACBL10ACBL8AC

data.display()

instructions = "L,6,L,4,R,12,L,6,R,12,R,12,L,8,L,6,L,4,R,12,L,6,L,10,L,10,L,6,L,6,R,12,R,12,L,8,L,6,L,4,R,12,L,6,L,10,L,10,L,6,L,6,R,12,R,12,L,8,L,6,L,4,R,12,L,6,L,10,L,10,L,6"
#data.addInstruction("A", ["L",6,"L",4,"R",12])
#data.addInstruction("B", ["L",6,"R",12,"R",12,"L",8])
#data.addInstruction("C", ["L",6,"L",10,"L",10,"L",6])

instructions = instructions.replace("L,6,L,4,R,12", "A").replace("L,6,R,12,R,12,L,8", "B").replace("L,6,L,10,L,10,L,6", "C")
print(instructions)
#print(data._instructions)
#for i in instructions.split(","):
#    data.updateRobot(i)
#    data.display()
#    input("i: " + i + "; pos: " + str(data.rPos) + "; dir: " + data.rDir[0] + "; Continue?")

machine.reset()
machine.store(0, 2)
machine.start(*[ord(c) for c in 
    instructions + "\n" + \
    "L,6,L,4,R,12\n" + \
    "L,6,R,12,R,12,L,8\n" + \
    "L,6,L,10,L,10,L,6\n" + \
    ("y\n" if data._liveDisplay else "n\n")
])
print(data.lastInputRaw)
