class Node():
  nodes = []
  def __init__(self, data):
    h = [data.popleft(), data.popleft()]
    self.children = [Node(data) for i in range(h[0])]
    self.meta = [data.popleft() for i in range(h[1])]
    Node.nodes.append(self)
  def value(self):
    return sum(self.meta) if len(self.children) < 1 else sum(self.children[m - 1].value() for m in self.meta if m <= len(self.children))

import loadFile, collections
print("Sum of all metadata: {p1}\nValue of root node: {p2}".format(p2 = Node(collections.deque(map(int, next(loadFile.loadfile(8)).split(" ")))).value(), p1 = sum(sum(n.meta) for n in Node.nodes)))
