from .. import intcode
from collections import deque
import os

class Robot:
  def __init__(self):
    self.x = 0
    self.y = 0
    self._tiles = {}
    self._direction = deque("^>v<")
    self.__inputColour = True
    self.xrange = [0,0]
    self.yrange = [0,0]
  @property
  def direction(self):
    return self._direction[0]
  @property
  def tileColour(self):
    return self.getTileColour(self.x, self.y)
  def getTileColour(self, x, y):
    return self._tiles.get((x, y), 0)
  def paintTile(self, colour):
    self._tiles[(self.x, self.y)] = colour
  def rotateAndMove(self, rotDir):
    self._direction.rotate(-1 if rotDir else 1) # rotDir = 1 -> right, 0 -> left)
    d = self.direction
    if d == "^":
      self.y += 1
      if self.y > self.yrange[1]:
        self.yrange[1] = self.y
    elif d == ">":
      self.x += 1
      if self.x > self.xrange[1]:
        self.xrange[1] = self.x
    elif d == "v":
      self.y -= 1
      if self.y < self.yrange[0]:
        self.yrange[0] = self.y
    else:
      self.x -= 1
      if self.x < self.xrange[0]:
        self.xrange[0] = self.x
  def recieveInput(self, inputval):
    if self.__inputColour:
      self.paintTile(inputval)
    else:
      self.rotateAndMove(inputval)
    self.__inputColour = not self.__inputColour

robot = Robot()

@intcode.IntCodeOperator(3)
def roboticInputOp(): # Overwrite default input IntCodeOp
  #print("Position: ({}, {}), colour: {}".format(robot.x, robot.y, robot.tileColour))
  return robot.tileColour

@intcode.IntCodeOperator(4)
def outputOp(a): # Overwrite default output IntCodeOp
  robot.recieveInput(a)

with open(os.path.dirname(__file__) + "/input.txt") as f:
  inputData = [int(n) for n in f.read().split(",")]

machine = intcode.IntCodeMachine(inputData)
machine.start()
print(len(robot._tiles))

machine.reset()
robot.__init__() # reset robot
robot._tiles[(0,0)] = 1
print("Position: ({}, {}), colour: {}".format(robot.x, robot.y, robot.tileColour))
machine.start()
for y in range(robot.yrange[1], robot.yrange[0] - 1, -1): # +y = up, so start from highest y
  row = (robot.getTileColour(x, y) for x in range(robot.xrange[0], robot.xrange[1] + 1))
  print("".join(("#" if c else " ") for c in row))
