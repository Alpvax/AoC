def printRow(recipes, e1, e2, display = False):
  def mapChar(i, c):
    if i == e1:
      return f"({c})"
    elif i == e2:
      return f"[{c}]"
    else:
      return f" {c} "
  if display:
    print("".join(mapChar(i, c) for i, c in enumerate(recipes)))

def doLoop(recipes, e1, e2):
  r1 = int(recipes[e1])
  r2 = int(recipes[e2])
  recipes += str(r1 + r2)
  l = len(recipes)
  e1 = (e1 + 1 + r1) % l
  e2 = (e2 + 1 + r2) % l
  printRow(recipes, e1, e2)
  return recipes, e1, e2

if __name__ == "__main__":
  improveAfter = 607331
  follow = 10

  recipes = "37"
  e1 = 0
  e2 = 1
  printRow(recipes, e1, e2)

  # Part 1
  while len(recipes) - 1 < improveAfter + follow:
    recipes, e1, e2 = doLoop(recipes, e1, e2)
  print("The scores of the {} recipes after the first {} are: {}".format(follow, improveAfter, recipes[improveAfter:improveAfter + follow]))

  # Part 2
  target = str(improveAfter)
  l = len(target)
  while True:
    index = recipes[-l-1].find(target)
    if index > 0:
      print("The target scores were found after position:", len(recipes) - l - 1 + index)
      break
    else:
      recipes, e1, e2 = doLoop(recipes, e1, e2)
