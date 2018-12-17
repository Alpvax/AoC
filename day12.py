from loadFile import loadfile
import re

INITIAL_STATE = "#.##.###.#.##...##..#..##....#.#.#.#.##....##..#..####..###.####.##.#..#...#..######.#.....#..##...#"

class Segment():
  def __init__(self, index, data):
    self.index = index
    self.data = data
  def __str__(self):
    return "".join(map(lambda b: "#" if b else ".", self.data))
  def __repr__(self):
    return "Segment@{}: {}".format(self.index, str(self))
  def __eq__(self, other):
    if isinstance(other, Segment):
      return other.index == self.index and other.data == self.data
    return NotImplemented
  def __hash__(self):
    return hash((self.index, str(self)))
  def match(self, patterns):
    return str(self) in patterns

class PotGeneration():
  def __init__(self, startState, offset = 0):
    if isinstance(startState, (str, list, tuple)):
      self.state = {i - offset: True for i,v in enumerate(startState) if v == "#"}
    elif isinstance(startState, dict):
      self.state = {k: v for k,v in startState.items() if v}
    elif isinstance(startState, PotGeneration):
      self.state = startState.state
    else:
      raise ValueError("startstate of type {} not supported".format(type(startState)))
    keys = sorted(self.state.keys())
    self.min = min(keys)
    self.max = max(keys)
  def segment(self, index):
    return Segment(index, [self.state.get(i, False) for i in range(index - 2, index + 3)])
  def allSegments(self):
    sections = set()
    for index in self.state.keys():
      sections.update(self.segment(index + i) for i in range(-2, 3))
    return sections
  def __str__(self, padding = 3):
    return "".join("#" if self.state.get(i, False) else "." for i in range(-padding, self.max + 1))
  def value(self):
    return sum(i for i, v in self.state.items() if v)

if __name__ == "__main__":
  mappings = {}
  pattern = re.compile(r"([#.]+) => ([#.])")
  for line in loadfile(12):
  #for line in loadfile("day12SampleData.txt"):
    m = pattern.match(line)
    mappings[m[1]] = m[2]

  patterns = [k for k, v in mappings.items() if v  == "#"]

  gen0 = PotGeneration(INITIAL_STATE)
  #gen0 = PotGeneration("#..#.#..##......###...###")
  #print("00: {}".format(str(gen0)))
  gen = gen0
  gens = {}
  delta = None
  deltaCount = 0
  for n in range(50000000000):
    gens[n] = gen = PotGeneration({seg.index: True for seg in gen.allSegments() if seg.match(patterns)})
    #print("{:02}: {}".format(n + 1, str(gen)))
    if n == 19:
      print(gen.value())
    if delta == None:
      delta = gen.value()
      deltaCount = 1
    else:
      d = gen.value() - gens[n-1].value()
      if d == delta:
        deltaCount += 1
        if deltaCount >= 10:
          print(f"Sequence stabilises after after {n - deltaCount} generations, incrementing by {delta} each generation.")
          print((50000000000 - n - 1) * delta + gen.value())
          break
      else:
        delta = d
        deltaCount = 1
