from collections import Counter

RACK_SERIAL = 9221

class Cell():
  def __init__(self, x, y, serial=RACK_SERIAL):
    self.x = x
    self.y = y
    rackid = x + 10
    self.power = int(str((rackid * y + serial) * rackid)[-3]) - 5

def getPowerCells(xSize, ySize, xcount = 3, ycount = 3):
  powergroups = Counter()
  for i in range(xSize - xcount):
    for j in range(ySize - ycount):
      powergroups["{},{}".format(i,j)] = sum(sum(Cell(i + x, j + y).power for x in range(xcount)) for y in range(ycount))
  return powergroups.most_common(1)[0]

if __name__ == "__main__":
  print("The 3x3 with the largest total power is:", getPowerCells(300, 300, 3, 3))
  c = Counter()
  for s in range(1, 301):
    pwr = getPowerCells(300,300, s, s)
    print("{},{} = {}".format(pwr[0], s, pwr[1]))
    c["{},{}".format(pwr[0], s)] = pwr[1]
  print("The largest total power area is:", c.most_common(1))
