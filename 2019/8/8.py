def printLayers(layers):
  for l in range(len(layers)):
    print("Layer", l + 1)
    for row in layers[l]:
      print(" ", row)
    print()

with open("input.txt") as f:
  layers = []
  layer = []
  r = 0
  while True:
    row = f.read(25)
    if len(row) < 25:
      print("Short row ({}):\n\"{}\"".format(len(row), row))
      break
    layer.append([int(c) for c in row])
    r += 1
    if r >= 6:
      r = 0
      layers.append(layer)
      layer = []

#printLayers(layers)

def checkSums(layers):
  for layer in layers:
    flatLayer = [n for row in layer for n in row]
    num0 = flatLayer.count(0)
    val = flatLayer.count(1) * flatLayer.count(2)
    yield (num0, val)

print(min(checkSums(layers)))

for j in range(6):
  row = []
  for i in range(25):
    for l in layers:
      n = l[j][i]
      if n != 2:
        row.append(str(n))
        break
  print("".join(row))
