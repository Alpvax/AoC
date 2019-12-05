#import timeit
#print(timeit.timeit('''
class Intersection:
  def __init__(self, pos, len1, len2):
    self.pos = pos
    self.l = [len1, len2]
    self.length = len1 + len2

class WireSegment:
  def __init__(self, start, end, wireLenToStart):
    self.start = start
    self.end = end
    self.startLen = wireLenToStart
  @property
  def minx(self):
    return min(self.start[0], self.end[0])
  @property
  def maxx(self):
    return max(self.start[0], self.end[0])
  @property
  def miny(self):
    return min(self.start[1], self.end[1])
  @property
  def maxy(self):
    return max(self.start[1], self.end[1])
  def __str__(self):
    return "WireSegment(startLen = {}; startPos = {}; endPos = {})".format(self.startLen, self.start, self.end)
    
class Wire:
  def __init__(self, name):
    self.name = name
    self.horz = []
    self.vert = []
    self.end = (0,0)
    self.length = 0
  def pushSegment(self, defn):
    d = defn[0]
    l = int(defn[1:])
    x,y = self.end
    if d == "U":
      y += l
    if d == "D":
      y -= l
    if d == "R":
      x += l
    if d == "L":
      x -= l
    #res = (
    #  (min(self.end[0], x), min(self.end[1], y)),
    #  (max(self.end[0], x), max(self.end[1], y)),
    #  (self.length, self.end),
    #)
    res = WireSegment(self.end, (x, y), self.length)
    #print(defn, "=>> Adding segment of length", l, "to", self.name, "( total length", self.length, ") ->", res)
    if d in ("U", "D"):
      self.vert.append(res)
    else:
      self.horz.append(res)
    self.end = (x, y)
    self.length += l
    return res

def parseInput(lines):
  wires = []
  for num,line in enumerate(lines, 1):
    wire = Wire("Wire " + str(num))
    for segment in line.split(","):
      wire.pushSegment(segment)
    wires.append(wire)
  return wires
    
def do_intersect(wireA, wireB):
  minDist = 0
  intersections = []
  for segA in wireA.horz:
    for segB in wireB.vert:
      x = segB.minx #minx = maxx for vert
      y = segA.miny #miny = maxy for horz
      dist = abs(x + y) #distance from origin
      if dist \
        and segA.minx <= x <= segA.maxx \
        and segB.miny <= y <= segB.maxy:
        if not minDist or dist < minDist:
          minDist = dist
        intersections.append(Intersection(
          (x, y),
          abs(segA.start[0] - x) + segA.startLen,
          abs(segB.start[1] - y) + segB.startLen,
        ))
  for segA in wireA.vert:
    for segB in wireB.horz:
      x = segA.minx #minx = maxx for vert
      y = segB.miny #miny = maxy for horz
      dist = abs(x + y) #distance from origin
      if dist \
        and segB.minx <= x <= segB.maxx \
        and segA.miny <= y <= segA.maxy:
        if not minDist or dist < minDist:
          minDist = dist
        intersections.append(Intersection(
          (x, y),
          abs(segA.start[1] - y) + segA.startLen,
          abs(segB.start[0] - x) + segB.startLen,
        ))
  print(minDist)
  return intersections

if __name__ == "__main__":
  #inputData = ["R8,U5,L5,D3", "U7,R6,D4,L4"]
  #inputData = ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]
  #wire1,wire2 = parseInput(inputData)
  with open("input.txt") as f:
    wire1,wire2 = parseInput(f)
  print(min([i.length for i in do_intersect(wire1, wire2)]))
#''', number=100)/100)