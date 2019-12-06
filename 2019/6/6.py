class Body:
  def __init__(self, name):
    self.name = name
    self.orbits = None
    self.children = []
  @property
  def numOrbits(self):
    return self.orbits.numOrbits + 1
  def __str__(self):
    return "{} (orbits {})".format(self.name, self.orbits.name if self.orbits else "UNKNOWN")
  def __repr__(self):
    return str(self)

class COM(Body):
  numOrbits = property(lambda s: 0)
  def __str__(self):
    return self.name

def parseLines(lines):
  map = {"COM": COM("COM")}
  def getBody(name):
    if name in map:
      return map[name]
    b = Body(name)
    map[name] = b
    return b
  for line in lines:
    obj1, obj2 = [getBody(name) for name in line.strip().split(")")]
    obj2.orbits = obj1
    obj1.children.append(obj2)
  return map


if True:
  with open("input.txt") as f:
    inputData = parseLines(f)
else:
  inputData = parseLines([
    "COM)B",
    "B)C",
    "C)D",
    "D)E",
    "E)F",
    "B)G",
    "G)H",
    "D)I",
    "E)J",
    "J)K",
    "K)L",
    "K)YOU",
    "I)SAN"
  ])

print(sum([b.numOrbits for b in inputData.values()]))

you = inputData["YOU"]
san = inputData["SAN"]
c = you.orbits
i = 0
trace = {}
while c.orbits:
  trace[c.name] = i
  c = c.orbits
  i += 1
print(trace)
c = san.orbits
i = 0
while c.orbits and c.name not in trace:
  trace[c.name] = i
  c = c.orbits
  i += 1
print(trace, i + trace[c.name])
