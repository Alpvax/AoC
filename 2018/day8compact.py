class Node():
  def __init__(self, data):
    h = [data.popleft(), data.popleft()]
    self.children = [Node(data) for i in range(h[0])]
    self.meta = [data.popleft() for i in range(h[1])]
  def v1(self): return sum(self.meta) + sum(c.v1() for c in self.children)
  def value(self): return sum(self.meta) if len(self.children) < 1 else sum(self.children[m - 1].value() for m in self.meta if m <= len(self.children))

import loadFile, collections
print("Sum of all metadata: {}\nValue of root node: {}".format(*[getattr(Node(collections.deque(map(int, next(loadFile.loadfile(8)).split(" ")))), m)() for m in ["v1", "value"]]))
