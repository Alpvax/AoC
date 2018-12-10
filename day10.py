from loadFile import loadfile
import re

class Point():
  def __init__(self, x, y, dx, dy):
    self.x = int(x)
    self.y = int(y)
    self.dx = int(dx)
    self.dy = int(dy)
  def pos(self, num):
    return (self.x + num * self.dx, self.y + num * self.dy)

if __name__ == "__main__":
  pattern = re.compile(r"position=<(?P<x>[ -]\d+), (?P<y>[ -]\d+)> velocity=<(?P<dx>[ -]\d+), (?P<dy>[ -]\d+)>")
  points = []
  for line in loadfile(10):
    m = pattern.match(line).groupdict()
    points.append(Point(m["x"], m["y"], m["dx"], m["dy"]))

#  for i in range(20000):
#    xlim, ylim = [max(vals) - min(vals) for vals in zip(*[p.pos(i) for p in points])]
#    print(i, xlim, ylim, xlim + ylim)
  sizes = [sum([max(vals) - min(vals) for vals in zip(*[p.pos(i) for p in points])]) for i in range(20000)]
  print(min(sizes), sizes.index(min(sizes)))

  with open("day10Out.txt", "w") as f:
    for point in points:
      print("{point.x},{point.y}", file = f)
