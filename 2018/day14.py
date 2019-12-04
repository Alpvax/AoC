def printRow(recipes, e1, e2, display = False):
  def mapChar(i, n):
    if i == e1:
      return f"({n})"
    elif i == e2:
      return f"[{n}]"
    else:
      return f" {n} "
  if display:
    print("".join(mapChar(i, n) for i, n in enumerate(recipes)))

def doLoop(recipes, e1, e2):
  r1 = recipes[e1]
  r2 = recipes[e2]
  r = r1 + r2
  recipes.extend(divmod(r, 10) if r > 9 else (r,))
  l = len(recipes)
  e1 = (e1 + 1 + r1) % l
  e2 = (e2 + 1 + r2) % l
  printRow(recipes, e1, e2)
  return recipes, e1, e2

if __name__ == "__main__":
  improveAfter = 607331
  follow = 10

  recipes = [3, 7]
  e1 = 0
  e2 = 1
  printRow(recipes, e1, e2)

  # Part 1
  while len(recipes) - 1 < improveAfter + follow:
    recipes, e1, e2 = doLoop(recipes, e1, e2)
  print("The scores of the {} recipes after the first {} are: {}".format(follow, improveAfter, "".join(str(n) for n in recipes[improveAfter:improveAfter + follow])))

  # Part 2
  index = "".join(str(n) for n in recipes).find(str(improveAfter))
  if index < 0:
    target = [int(n) for n in str(improveAfter)]
    l = len(target)
    while True:
      if recipes[-l-1:-1] == target:
        index = len(recipes) - l
        break
      elif recipes[-l:] == target:
        index = len(recipes) - l + 1
        break
      recipes, e1, e2 = doLoop(recipes, e1, e2)
  print("The target scores were found after position:", index)
