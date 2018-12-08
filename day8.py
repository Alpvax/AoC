from loadFile import loadfile
from collections import deque

class Node():
  nodes = []
  def __init__(self, data):
    self. numChild = data.popleft()
    self. numMeta = data.popleft()
    self.children = []
    for i in range(self.numChild):
      self.children.append(Node(data))
    self.meta = []
    for i in range(self.numMeta):
      self.meta.append(data.popleft())
    Node.nodes.append(self)
  @property
  def value(self):
    if self.numChild < 1:
      return sum(self.meta)
    else:
      total = 0
      for i in [m - 1 for m in self.meta]:
        if i < self.numChild:
          total += self.children[i].value
      return total

if __name__ == "__main__":
  data = deque(map(int, next(loadfile(8)).split(" ")))
  #data = deque(map(int, "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2".split(" ")))
  root = Node(data)
  print("Sum of all metadata:", sum(sum(n.meta) for n in Node.nodes))
  print("Value of root node:", root.value)
