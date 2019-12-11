import os, math, itertools

class Asteroid():
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.sees = {}
  def checkSight(self, *others):
    for other in others:
      if other != self:
        a = math.atan2(other.y - self.y, other.x - self.x) + math.pi / 2
        if a < 0:
          a += 2 * math.pi
        m2 = (other.y - self.y) ** 2 + (other.x - self.x) ** 2
        sa = self.sees.get(a, [])
        sa.append((m2, other))
        self.sees[a] = sorted(sa)
  @property
  def numSeen(self):
    return len(self.sees)
  def __str__(self):
    return "({},{})".format(self.x, self.y)
  def __repr__(self):
    return "Asteroid({},{})".format(self.x, self.y)
  def __lt__(self, other):
    return self.numSeen < other.numSeen

def parseAsteroids(lines):
  asteroids = []
  y = 0
  for line in lines:
    asteroids += [Asteroid(x, y) for x in range(len(line)) if line[x] == "#"]
    y += 1
  return asteroids

if True:
  with open(os.path.dirname(__file__) + "/input.txt") as f:
    asteroids = parseAsteroids(f)
else:
  asteroids = parseAsteroids([
    ".#..##.###...#######",
    "##.############..##.",
    ".#.######.########.#",
    ".###.#######.####.#.",
    "#####.##.#.##.###.##",
    "..#####..#.#########",
    "####################",
    "#.####....###.#.#.##",
    "##.#################",
    "#####.##.###..####..",
    "..######..##.#######",
    "####.##.####...##..#",
    ".#####..#.######.###",
    "##...#.##########...",
    "#.##########.#######",
    ".####.#.###.###.#.##",
    "....##.##.###..#####",
    ".#.#.###########.###",
    "#.#.#.#####.####.###",
    "###.##.####.##.#..##",
  ])

for a in asteroids:
  a.checkSight(*asteroids)
dest = max([(a.numSeen, a) for a in asteroids])[1]
print(dest.numSeen)

#target_angles = (dest.sees[a] for a in sorted(dest.sees.keys()))
#print(list(zip(*target_angles)))
#print(",\n".join(str(v) for v in target_angles))
#print(",\n".join(str(v) for v in itertools.zip_longest(*[dest.sees[a] for a in sorted(dest.sees.keys())])))
targets = itertools.chain.from_iterable(itertools.zip_longest(*[dest.sees[a] for a in sorted(dest.sees.keys())]))
tnum = 0
for target in targets:
  if target:
    tnum += 1
    if tnum >= 200:
      break
print(target[1].x*100 + target[1].y)
