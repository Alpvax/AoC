from loadFile import loadfile
import re

TILES = {}#"500,0": "+"}
Y_MIN = 10000 # higher than at least 1 of the values (for min to work)
Y_MAX = 0

def getTile(x, y):
  return TILES.get(f"{x},{y}", ".")

def setTile(x, y, material):
  TILES[f"{x},{y}"] = material

def spread(x, y):
  if y + 1 > Y_MAX:
    setTile(x, y, "|")
    print(f"Hit the bottom at ({x},{y})")
    return
  if getTile(x, y + 1) in ".|":
    setTile(x, y, "|")
    spread(x, y + 1)
  if getTile(x, y + 1) in "~#":
    left = x
    while getTile(left, y) in ".|" and getTile(left, y + 1) in "~#":
      left -= 1
    right = x
    while getTile(right, y) in ".|" and getTile(right, y + 1) in "~#":
      right += 1
    row = [getTile(i, y) for i in range(left, right + 1)]
    tile = "|"
    def gapsBelow(left, right, y):
      return [left + i for i, t in enumerate(getTile(i, y + 1) for i in range(left, right + 1)) if t in ".|"]
    if len(gapsBelow(left, right, y)) < 1:#row[0] == "#" and row [-1] == "#":
      tile = "~"
    else:
      for gapx in gapsBelow(left, right, y):
        spread(gapx, y + 1)
      if len(gapsBelow(left, right, y)) < 1: # Repeat spread if gaps are now filled
        spread(x, y)
    for i in range(left, right + 1): # Fill row
      if getTile(i, y) in ".|":
        setTile(i, y, tile)
    print(f"\n{left} - {right} @ {y}:", row)
    print(f"{left} - {right} @ {y + 1}:", [getTile(i, y + 1) for i in range(left, right + 1)])

def printTiles():
  area = [[min(vals), max(vals) + 1] for vals in zip(*[map(int, k.split(",")) for k in TILES.keys()])]
  for y in range(*area[1]):
    for x in range(*area[0]):
      print(getTile(x, y), end="")
    print()

if __name__ == "__main__":
  reval = r"(\d+)(?:\.{2}(\d+))?"
  px = re.compile(r"x=" + reval)
  py = re.compile(r"y=" + reval)
  for line in loadfile(17, sample=False):
    xr = px.search(line)
    xlim = [int(xr[1]), int(xr[2]) + 1 if xr[2] != None else int(xr[1]) + 1]
    yr = py.search(line)
    ylim = [int(yr[1]), int(yr[2]) + 1 if yr[2] != None else int(yr[1]) + 1]
    Y_MAX = max(Y_MAX, ylim[1] - 1)
    Y_MIN = min(Y_MIN, ylim[0])
    for x in range(xlim[0], xlim[1]):
      for y in range(ylim[0], ylim[1]):
        setTile(x, y, "#")
  #printTiles()

  x = 500
  y = 0
  spread(x, y + 1)
  print(len([t for t in TILES if t in "~|"]))
  #printTiles()
