import re, math, os

class ReactantQuantity:
  def __init__(self, name, quantity):
    self.name = name.strip()
    self.qty = int(quantity)
  def __repr__(self):
    return self.name + "(" + str(self.qty) + ")"

class Recipe:
  def __init__(self, output, *ingredients):
    self.output = output
    self.inputs = ingredients
  @property
  def name(self):
    return self.output.name
  @property
  def qty(self):
    return self.output.qty
  def getRequirements(self, number=1):
    return [ReactantQuantity(r.name, r.qty * number) for r in self.inputs]
  def __repr__(self):
    return ", ".join(str(i) for i in self.inputs) + " => " + str(self.output)

class Processor:
  def __init__(self):
    self.recipes = {}
    self.amounts = {}
    self.oreUsed = 0
  def addRecipe(self, recipe):
    name = recipe.output.name
    if name in self.recipes:
      print("WARNING! Duplicate output:", name)
    self.recipes[name] = recipe
  def withdraw(self, name, quantity):
    #print(f"Attempting to withdraw {quantity} {name} from stockpile:{self.amounts}")
    if name == "ORE":
      #print(f"Extracting {quantity} {name}")
      self.oreUsed += quantity
    else:
      qty = self.amounts.get(name, 0)
      #print(f"Stock of {name}: {qty}")
      if qty < quantity:
        qty = self.craft(name, quantity - qty)
      #print(f"Withdrawing {quantity} {name}")
      self.amounts[name] = qty - quantity
  def craft(self, name, quantity):
    r = self.recipes.get(name)
    numCrafts = math.ceil(quantity / r.qty)
    for req in r.getRequirements(numCrafts):
      self.withdraw(req.name, req.qty)
    a = self.amounts.get(name, 0)
    newQty = a + numCrafts * r.qty
    #print(f"Crafted {numCrafts * r.qty} {name}, total quantity now {newQty}")
    self.amounts[name] = newQty
    return newQty
  def __repr__(self):
    return "\n".join(str(r) for r in self.recipes.values())

def parse(lines):
  proc = Processor()
  pattern = re.compile(r"(\d+)\s([A-Z]+)")
  for line in lines:
    i,o = line.split("=>")
    o = ReactantQuantity(*pattern.search(o).group(2,1))
    i = [ReactantQuantity(*m.group(2,1)) for m in pattern.finditer(i)]
    proc.addRecipe(Recipe(o, *i))
  return proc

if True:
  with open(os.path.dirname(__file__) + "/input.txt") as f:
    proc = parse(f)
else:
  proc = parse([
  #  "10 ORE => 10 A",
  #  "1 ORE => 1 B",
  #  "7 A, 1 B => 1 C",
  #  "7 A, 1 C => 1 D",
  #  "7 A, 1 D => 1 E",
  #  "7 A, 1 E => 1 FUEL"
  #])
    "9 ORE => 2 A",
    "8 ORE => 3 B",
    "7 ORE => 5 C",
    "3 A, 4 B => 1 AB",
    "5 B, 7 C => 1 BC",
    "4 C, 1 A => 1 CA",
    "2 AB, 3 BC, 4 CA => 1 FUEL"
  ])

#proc = parse(inputData)
print(proc)
proc.withdraw("FUEL", 1)
used1 = proc.oreUsed
print(used1)
fuel = 1
while proc.oreUsed < 1E+12:
  remainingOre = 1E+12 - proc.oreUsed
  d = int(remainingOre // used1)
  if d < 1:
    break
  proc.withdraw("FUEL", d)
  fuel += d
  print(f"Used {proc.oreUsed:,d} ore to produce {fuel:,d} fuel")
print(fuel)
proc.withdraw("FUEL", 1)
print(f"Would use {proc.oreUsed:,d} ore to produce {fuel + 1:,d} fuel") # Check not enough ore remaining for a final fuel
