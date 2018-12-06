from loadFile import loadfile
from collections import Counter

class Point():
  __allPoints = {}
  @classmethod
  def get(cls, x, y, points = []):
    k = "{},{}".format(x, y)
    if k in cls.__allPoints:
      return cls.__allPoints[k]
    p = Point(x, y)
    p.calcDists(points)
    cls.__allPoints[k] = p
    return p
  @classmethod
  def points(cls):
    return cls.__allPoints.values()
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.dists = Counter()
  def __repr__(self):
    return str(self)
  def __str__(self):
    return "Point({p.x}, {p.y})".format(p=self)
  def calcDists(self, points):
    self.dists.update(dict([(k, self.dist(*p)) for k, p in enumerate(points)]))
  def closest(self, dist = False):
    check = self.dists.most_common()[:-3:-1]
    if check[0][1] == check[1][1]:
      return None if not dist else (None, -1)
    return check[0] if dist else check[0][0]
  def dist(self, x, y):
    return abs(self.x - x) + abs(self.y - y)

def getDistCount(points, xlim, ylim, displayLen = False):
  if displayLen == True:
    displayLen = len(str(int(len(points) / 26 + 0.99))) # Maximum length of the postfix number
  for j in incRange(ylim):
    for i in incRange(xlim):
      id, d = Point.get(i, j, points).closest(True)
      if displayLen > 0:
        if id == None:
          c = "." * displayLen
        else:
          c = chr(ord("a") + id)
          if d == 0:
            c = c.upper()
          if displayLen > 1:
            c += str(id // 26 + 1)
        print(c, end=" ")
    if displayLen > 0:
      print("")

def incRange(limits):
  for i in range(limits[0], limits[1] + 1):
    yield i

if __name__ == "__main__":
  points = [(lambda x,y: [int(x), int(y)])(*p.split(",")) for p in loadfile(6)]
  threshold = 10000
  #points = [[1, 1], [1, 6], [8, 3], [3, 4], [5, 5], [8, 9]] # Sample
  #threshold = 32 # Sample

  xlim, ylim = [[min(vals) - 1, max(vals) + 1] for vals in zip(*points)]
  #print(xlim, ylim)

  getDistCount(points, xlim, ylim)#, True)

  edges = set()
  def excludeArea(x, y):
    area = Point.get(x, y).closest()
    if area != None:
      edges.add(area)
  for i in xlim:                      # Left and right edges
    for j in incRange(ylim): # Each row
      excludeArea(i, j)
  for j in ylim:                      # Top and bottom edges
    for i in incRange(xlim): # Each column
      excludeArea(i, j)

  # Part 1
  c = Counter()
  for p in map(lambda point: point.closest(), Point.points()):
    if p != None and not p in edges:
      c[p] += 1
  print("Largest finite area:", c.most_common(1)[0][1])

  # Part 2
  print("Total number of tiles with total distance to all points < {}: {}".format(threshold,
    len([p for p in Point.points() if sum(p.dists.values()) < threshold])))
