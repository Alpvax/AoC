from loadFile import loadfile
from functools import total_ordering
import re

class NodeMeta(type):
  def __call__(cls, key, *args, **kwarg):
    if key in cls.items:
      return cls.items[key]
    n = super().__call__(key, *args, **kwarg)
    cls.items[key] = n
    return n

@total_ordering
class Node(metaclass=NodeMeta):
  items = {}
  order = {}
  rules = []
  def __init__(self, key):
    self.key = key
    self.children = set()
    self.parents = set()
    self.duration = ord(self.key) - 4 # (60 - 65 + 1) (ord("A") = 65)
    self.sortIndex = key
  def addChild(self, child):
    if type(child) != Node:
      child = Node(child)
    child.parents.add(self)
    self.children.add(child)
  @property
  def root(self):
    return len(self.parents) < 1
  def __iter__(self):
    yield from sorted(self.children)
  def __str__(self):
    return "Node:{}{}".format(self.key, sorted([n.key for n in self.children]))
  def __repr__(self):
    return str(self)
  def __hash__(self):
    return hash(self.key)
  def __eq__(self, other):
    if hasattr(other, "key"):
      return self.key == other.key
    return NotImplemented
  def __lt__(self, other):
    if hasattr(other, "sortIndex"):
      return self.sortIndex < other.sortIndex
    return NotImplemented

def sortNodes():
  sortedNodes = []
  nodes = set(node for node in Node.items.values() if node.root)
  while len(nodes) > 0:
    for node in sorted(nodes, key=lambda n: n.key):
      if len([p for p in node.parents if p.key not in sortedNodes]) < 1: # If parents are all added
        node.sortIndex = len(sortedNodes)
        sortedNodes.append(node.key)
        nodes.remove(node)
        nodes.update(node.children)
        break
  return sortedNodes

def build(order, numWorkers = 4 + 1):
  remaining = set(Node(k) for k in order)
  current = {}
  sec = 0
  while len(remaining) > 0:
    if len(current) < numWorkers:
      available = [node for node in sorted(remaining) if node not in current and len(remaining.intersection(node.parents)) < 1][0: numWorkers - len(current)]
#      print(current, available)
      for node in available:
        current[node] = node.duration
#      print(current)
    step = min(current.values())
    sec += step
#    print("Currently building: {}\nSkipping {} secs, total time ellapsed: {}".format({n.key: d for n,d in current.items()}, step, sec))
    for n,d in dict(current).items():
      d -= step
      if d < 1:
        del current[n]
        remaining.remove(n)
      else:
        current[n] = d
  return sec


if __name__ == "__main__":
  pattern = re.compile(r"^Step ([A-Z]) .+ step ([A-Z])")
  for line in loadfile(7):
    m = pattern.match(line)
    Node(m[1]).addChild(m[2])

  order = sortNodes()
  print("Sorted order:", "".join(order))

  print("Total build time:", build(order))
