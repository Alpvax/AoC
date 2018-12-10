from loadFile import loadfile
import re

class Point():
  def __init__(self, x, y):
    self.x = int(x)
    self.y = int(y)
  def __eq__(self, other):
    try:
      x = getattr(other, "x") # Try obj.x
      y = getattr(other, "y") # Try obj.y
    except AttributeError as e:
      print(e)
      try:
        x = other[0] # Fallback to first number of tuple/list
        y = other[1] # Fallback to second number of tuple/list
      except TypeError as e:
        print(e)
        return NotImplemented
    return self.x == x and self.y == y
  def __hash__(self):
    return hash((self.x, self.y))
  def __str__(self):
    return "{},{}".format(self.x, self.y)
  def __repr__(self):
    return "Point({})".format(self)
  def __iter__(self):
    yield from [self.x, self.y]

class MovingPoint(Point):
  def __init__(self, x, y, dx, dy):
    super().__init__(x, y)
    self.dx = int(dx)
    self.dy = int(dy)
  def pos(self, num):
    return (self.x + num * self.dx, self.y + num * self.dy)

if __name__ == "__main__":
  pattern = re.compile(r"position=<(?P<x>[ -]\d+), (?P<y>[ -]\d+)> velocity=<(?P<dx>[ -]\d+), (?P<dy>[ -]\d+)>")
  points = []
  for line in loadfile(10):
    m = pattern.match(line).groupdict()
    points.append(MovingPoint(m["x"], m["y"], m["dx"], m["dy"]))

  sizes = [sum([max(vals) - min(vals) for vals in zip(*[p.pos(i) for p in points])]) for i in range(20000)]
  minSizeIndex = sizes.index(min(sizes))

  unique = set(Point(*p.pos(minSizeIndex)) for p in points)
  mins = [min(v) for v in zip(*unique)]
  out = {}
  for point in unique:
    x = point.x - mins[0]
    y = point.y - mins[1]
    r = out.get(y, [])
    r.append(x)
    out[y] = r
  for i in range(max(out.keys()) + 1):
    if i in out:
      r = sorted(out[i])
      o = ""
      l = 0
      for n in r:
        o += " " * (n - l) + "#"
        l = n + 1
      print(o)
    else:
      print()
  print("\nIndex of smallest area:", minSizeIndex)
