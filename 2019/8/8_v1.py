if True:
  with open("input.txt") as f:
    inputData = [int(n) for n in f.read().strip()]
    size = [25, 6]
else:
  inputData = [int(n) for n in "123456789012"]
  size = [3, 2]


layerSize = size[0] * size[1]
print(len(inputData), len(inputData) // layerSize, len(inputData) % layerSize)

layers = []
l = 0
i = 0
while i < len(inputData):
  layers.append([])
  for j in range(size[1]):
    i += size[0] * j
    layers[l].append(inputData[i: i + size[0]])
  i += size[0]
  l += 1

for l in range(len(layers)):
  print("Layer", l + 1)
  for row in layers[l]:
    print(" ", row)
  print()
