from loadFile import loadfile
from collections import Counter
import re

class NodeMeta(type):
  def __call__(cls, id, *args, **kwarg):
    if id in cls.ids:
      return cls.ids[id]
    n = super().__call__(id, *args, **kwarg)
    cls.ids[id] = n
    return n

class Node(metaclass=NodeMeta):
  ids = {}
  def __init__(self, id):
    self.id = id
    self.children = set()
    self.parents = set()
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
    return "Node:{}{}".format(self.id, sorted([n.id for n in self.children]))
  def __repr__(self):
    return str(self)

def nodeRecurse(node, index, callback):
  print(index, node)
  index = callback(node, index)
  for n in node.children:
    index = nodeRecurse(n, index, callback)
  return index

if __name__ == "__main__":
  pattern = re.compile(r"^Step ([A-Z]) .+ step ([A-Z])")
  for line in loadfile(7):
    m = pattern.match(line)
    Node(m[1]).addChild(m[2])

  nodeOrder = {}
  def setNodePos(node, index):
    nodeOrder[node.id] = index
    return  index + 1

  i = 0
  for node in sorted(Node.ids.values(), key=lambda n: n.id):
    if node.root:
      i += nodeRecurse(node, i, setNodePos)
  print("".join(reversed([id[0] for id in Counter(nodeOrder).most_common()])))
