from loadFile import loadfile
import re

overlaps = set()

class Region():
  def __init__(self, id, x, y, w, h):
    self.id = id
    self.l = self.x = int(x)
    self.t = self.y = int(y)
    self.w = int(w)
    self.h = int(h)
    self.r = self.x + self.w
    self.b = self.y + self.h
    self.overlap = False

  def area(self, other):  # returns None if rectangles don't intersect
    xmin = max(self.l, other.l)
    xmax = min(self.r, other.r)
    ymin = max(self.t, other.t)
    ymax = min(self.b, other.b)
    if(xmax - xmin > 0 and ymax - ymin > 0):
      self.overlap = other.overlap = True
      for i in range(xmin, xmax):
        for j in range(ymin, ymax):
          overlaps.add(str(i) + "x" + str(j))

if __name__ == "__main__":
  pattern =  re.compile(r"#(?P<id>\d+)\s@\s(?P<x>\d+),(?P<y>\d+)\s(?P<w>\d+)x(?P<h>\d+)")
  regions = []
  for line in loadfile(3):
    m = pattern.match(line)
    #print(m.groupdict())
    r = Region(**m.groupdict())
    for r1 in regions:
      r1.area(r)
    regions.append(r)
  print(len(overlaps))
  print([r.id for r in regions if not r.overlap])
