
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
    res = (
      (min(self.end[0], x), min(self.end[1], y)),
      (max(self.end[0], x), max(self.end[1], y)),
      (self.length, self.end),
    )
    print(defn, "=>> Adding segment of length", l, "to", self.name, "( total length", self.length, ") ->", res)
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
      x = segB[0][0]
      y = segA[0][1]
      dist = abs(x + y)
      if dist \
        and segA[0][0] <= x and x <= segA[1][0] \
        and segB[0][1] <= y and y <= segB[1][1]:
        if not minDist or dist < minDist:
          minDist = dist
        intersections.append((
          (x, y),
          segA[2][0] + abs(segA[2][1][0]) \
          + segB[2][0] + abs(segB[2][1][1])
        ))
  for segA in wireA.vert:
    for segB in wireB.horz:
      x = segA[0][0]
      y = segB[0][1]
      dist = abs(x + y)
      if dist \
        and segB[0][0] <= x and x <= segB[1][0] \
        and segA[0][1] <= y and y <= segA[1][1]:
        if not minDist or dist < minDist:
          minDist = dist
        intersections.append((
          (x, y),
          segA[2][0] + abs(segA[2][1][1]) \
          + segB[2][0] + abs(segB[2][1][0])
        ))
  print(minDist)
  return intersections

if __name__ == "__main__":
  inputData = ["R8,U5,L5,D3", "U7,R6,D4,L4"]
  wire1,wire2 = parseInput(inputData)
  print(wire1)
  print(wire2)
  #with open("input.txt") as f:
  #  wire1,wire2 = parseInput(f)
  print([i[1] for i in do_intersect(wire1, wire2)])