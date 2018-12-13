from loadFile import loadfile
from collections import deque

class CartCollision(Exception):
  def __init__(self, x, y):
    super().__init__(f"Collision at {x},{y}")

class Track():
  def __init__(self, x, y, char):
    self.x = x
    self.y = y
    self.char = char
    self.cart = None
  def enter(self, cart):
    if self.cart:
      raise CartCollision(self.x, self.y)
    self.cart = cart
    if self.char == "/":
      if cart.facing in [0, 2]: # Vertical
        cart.rotate(-1) # Right
      else: # Horizontal
        cart.rotate(1) # Left
    elif self.char == "\\":
      if cart.facing in [0, 2]: # Vertical
        cart.rotate(1) # Left
      else: # Horizontal
        cart.rotate(-1) # Right
    elif self.char == "+":
      cart.rotate() # According to previous intersection rotation
    else:
      pass # Do not rotate

class Cart():
  def __init__(self, x, y, facing):
    self.x = x
    self.y = y
    self.__facing = deque([0, 1, 2, 3]) # 0 = Up, 1 = Right, 2 = Down, 3 = Left
    self.__facing.rotate(-facing)
    self.__rotate = deque([1, 0, -1]) # 1 = left, 0 = straight, -1 = right
  @property
  def facing(self):
    return self.__facing[0]
  def rotate(self, direction = None):
    if direction != None:
      r = self.__rotate[0]
      self.__rotate.rotate(-1)
    self.__facing.rotate(r)
  def move(self, tracks):
    tracks[f"{self.x},{self.y}"].cart = None
    if self.facing == 0: # Up (^)
      self.y -= 1
    elif self.facing == 1: # Right (>)
      self.x += 1
    elif self.facing == 2: # Down (v)
      self.y += 1
    elif self.facing == 3: # Left (<)
      self.x -= 1
    tracks[f"{self.x},{self.y}"].enter(self)
