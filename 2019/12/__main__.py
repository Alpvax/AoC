import re, itertools

class Planet:
  def __init__(self, x, y, z, name):
    self.name = name
    self.x = int(x)
    self.y = int(y)
    self.z = int(z)
    self.vx = 0
    self.vy = 0
    self.vz = 0
  @property
  def pot(self):
    return abs(self.x) + abs(self.y) + abs(self.z)
  @property
  def kin(self):
    return abs(self.vx) + abs(self.vy) + abs(self.vz)
  @property
  def energy(self):
    return self.pot * self.kin
  def updateVelocities(self, other):
    dx = other.x - self.x
    if dx: # Non-zero
      dx /= abs(dx)
      dx = int(dx)
      self.vx += dx
      other.vx -= dx
    dy = other.y - self.y
    if dy: # Non-zero
      dy /= abs(dy)
      dy = int(dy)
      self.vy += dy
      other.vy -= dy
    dz = other.z - self.z
    if dz: # Non-zero
      dz /= abs(dz)
      dz = int(dz)
      self.vz += dz
      other.vz -= dz
  def updatePos(self):
    self.x += self.vx
    self.y += self.vy
    self.z += self.vz
  def __str__(self):
    return "pos=<x={s.x: 3d}, y={s.y: 3d}, z={s.z: 3d}>, vel=<x={s.vx: 3d}, y={s.vy: 3d}, z={s.vz: 3d}>".format(s=self)
  def __repr__(self):
    return f"Planet {self.name}({self.x} + {self.vx}, {self.y} + {self.vy}, {self.z} + {self.vz})"

def parse(lines):
  planets = []
  for line in lines:
    m = re.search(r"x=(-?\d+), y=(-?\d+), z=(-?\d+)", line)
    planets.append(Planet(*m.groups(), len(planets)))
  return planets

def update(planets):
  for a, b in itertools.combinations(planets, 2):
    a.updateVelocities(b)
  for p in planets:
    p.updatePos()

def output(planets):
  print("\n".join(str(p) for p in planets))

if True:
  inputData = [ # Input
    "<x=-19, y=-4, z=2>",
    "<x=-9, y=8, z=-16>",
    "<x=-4, y=5, z=-11>",
    "<x=1, y=9, z=-13>"
  ]
else:
  #inputData = [ # Sample 1
  #  "<x=-1, y=0, z=2>",
  #  "<x=2, y=-10, z=-7>",
  #  "<x=4, y=-8, z=8>",
  #  "<x=3, y=5, z=-1>"
  #]
  inputData = [ # Sample 2
    "<x=-8, y=-10, z=0>",
    "<x=5, y=5, z=10>",
    "<x=2, y=-7, z=3>",
    "<x=9, y=-8, z=-3>"
  ]
planets = parse(inputData)
output(planets)
for i in range(1000):
  update(planets)
output(planets)
print(sum(p.energy for p in planets))
