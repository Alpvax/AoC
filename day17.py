from loadFile import loadfile
import re

TILES = {}#"500,0": "source"}

def key(x, y):
  return f"{x},{y}"

if __name__ == "__main__":
  def getTile(x, y):
    return TILES.get(key(x, y), "sand")
  reval = r"(\d+)(?:\.{2}(\d+))?"
  px = re.compile(r"x=" + reval)
  py = re.compile(r"y=" + reval)
  for line in loadfile(17, sample=True):
    xr = px.search(line)
    xlim = [int(xr[1]), int(xr[2]) if xr[2] != None else int(xr[1]) + 1]
    yr = py.search(line)
    ylim = [int(yr[1]), int(yr[2]) if yr[2] != None else int(yr[1]) + 1]
    for x in range(xlim[0], xlim[1]):
      for y in range(ylim[0], ylim[1]):
        TILES[key(x, y)] = "clay"
  #print(TILES)
  area = [[min(vals), max(vals)] for vals in zip(*[map(int, k.split(",")) for k in TILES.keys()])]
  print(area)
  x = 500
  y = 0
  while y < area[1][1]:
    tile = getTile(x, y)
    below = getTile(x, y + 1)
    if below in ["sand", "wet_sand"]:
      y += 1
      continue
    else:
      print(f"Spreading above {below} at ({x}, {y})")
      break
