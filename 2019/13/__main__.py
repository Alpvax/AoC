from .. import intcode
import os

tileTypes = {
  0: " ", # an empty tile. No game object appears in this tile.
  1: "#", # a wall tile. Walls are indestructible barriers.
  2: "x", # a block tile. Blocks can be broken by the ball.
  3: "-", # a horizontal paddle tile. The paddle is indestructible.
  4: "O", # a ball tile. The ball moves diagonally and bounces off objects.
}

class Screen:
  def __init__(self):
    self.tiles = {}
    self.minx = 0
    self.maxx = 0
    self.miny = 0
    self.maxy = 0
    self.__currentInput = []
    self.score = 0
    self.ballX = None
    self.paddleX = None
  def getTile(self, x, y):
    return self.tiles.get((x, y), 0)
  def setTile(self, x, y, val):
    self.tiles[(x, y)] = val
    if val == 4: # Ball
      self.ballX = x
    if val == 3: # Paddle
      self.paddleX = x
    self.minx = min(self.minx, x)
    self.maxx = max(self.maxx, x)
    self.miny = min(self.miny, y)
    self.maxy = max(self.maxy, y)
  def receiveInput(self, val):
    if len(self.__currentInput) == 2:
      if self.__currentInput == [-1, 0]: # Score output
        self.score = val
      else:
        self.setTile(*self.__currentInput, val)
      self.__currentInput.clear()
    else:
      self.__currentInput.append(val)
  def output(self):
    print("Score:",self.score)
    for y in range(self.miny, self.maxy + 1):
      print("".join(tileTypes.get(self.getTile(x, y)) for x in range(self.minx, self.maxx + 1)))

screen = Screen(True)
autopilot = False
outputFrames = True

@intcode.IntCodeOperator(4)
def screenOutputOp(a):
  screen.receiveInput(a)

@intcode.IntCodeOperator(3)
def joyInputOp():
  if outputFrames: screen.output()
  if autopilot:
    d = screen.ballX - screen.paddleX
    if d:
      return int(d / abs(d))
    else:
      return 0
  else:
    return {
      "a": -1,
      "l": -1,
      "d": 1,
      "r": 1,
    }.get(input("Enter joystick input: (a=left,d=right, else neutral)\n").lower(), 0)

with open(os.path.dirname(__file__) + "/input.txt") as f:
  inputData = [int(n) for n in f.read().split(",")]

machine = intcode.IntCodeMachine(inputData)
machine.start()
print(len([t for p,t in screen.tiles.items() if t == 2]))
machine.reset()
machine.store(0, 2)
machine.start()
print(screen.score)
