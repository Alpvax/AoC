from loadFile import loadfile
from collections import deque

class CartCollision(Exception):
  def __init__(self, x, y, *carts):
    super().__init__("Collision between carts: {c}; at {x},{y}".format(c=" and ".join([str(c.cartID) for c in carts]), x=str(x), y=str(y)))
    self.carts = carts

class Track():
  def __init__(self, x, y, char, cart = None):
    self.x = x
    self.y = y
    self.char = char
    self.cart = cart
  def enter(self, cart):
    if self.cart:
      raise CartCollision(self.x, self.y, self.cart, cart)
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
  def __init__(self, cartID, x, y, facing):
    self.cartID = cartID
    self.x = x
    self.y = y
    self.__facing = deque([0, 1, 2, 3]) # 0 = Up, 1 = Right, 2 = Down, 3 = Left
    self.__facing.rotate(-facing)
    self.__rotate = deque([1, 0, -1]) # 1 = left, 0 = straight, -1 = right
  @property
  def facing(self):
    return self.__facing[0]
  def rotate(self, direction = None):
    if direction == None:
      direction = self.__rotate[0]
      self.__rotate.rotate(-1)
    self.__facing.rotate(direction)
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
  def __lt__(self, other):
    return self.y < other.y and self.x < other.x
  def __str__(self):
    return "^>v<"[self.facing]
  def __repr__(self):
    return f"Cart({self.cartID})@{self.x},{self.y} Facing:{str(self)}"

if __name__ == "__main__":
  tracks = {}
  carts = {}
  cartID = 0
  for y, line in enumerate(loadfile(13)):
  #for y, line in enumerate(loadfile("day13SampleData.txt")):
    for x, char in enumerate(line):
      if char == " ":
        continue
      pos = f"{x},{y}"
      cart = None
      if char in "^>v<":
        carts[cartID] = cart = Cart(cartID, x, y, "^>v<".index(char))
        cartID += 1
        char = "-" if char in "<>" else "|"
      tracks[pos] = Track(x, y, char, cart)

  collisionNum = 0
  while len(carts) > 1:
    try:
      for cart in sorted(carts.values()):
        cart.move(tracks)
    except CartCollision as e:
      print(e)
      for c in e.carts:
        if c.cartID in carts:
          del carts[c.cartID]
      print(sorted(carts.values(), key = lambda c: c.cartID))
      if collisionNum == 0:
        print(e)
