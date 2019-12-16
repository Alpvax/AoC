import re, math

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
  def getRequirements(self, number=1):
    print("Creating {} {} from {}".format(self.output.qty * number, self.output.name, ", ".join(str(i) for i in self.inputs)))
    return [ReactantQuantity(r.name, r.qty * number) for r in self.inputs]
  def __repr__(self):
    return ", ".join(str(i) for i in self.inputs) + " => " + str(self.output)

class Processor:
  def __init__(self):
    self.patterns = {}
    self.amounts = {}
    self.oreUsed = 0
  def addRecipe(self, recipe):
    name = recipe.output.name
    if name in self.patterns:
      print("WARNING! Duplicate output:", name)
    self.patterns[name] = recipe
  def request(self, name, quantity = 1):
    recipe = self.patterns.get(name)
    qty = math.ceil(quantity / recipe.output.qty)
    requirements = recipe.getRequirements(qty)
    for r in requirements:
      self.withdraw(r.name, r.qty)
  def withdraw(self, name, quantity):
    print(f"Attempting to withdraw {quantity} {name}")
    if name == "ORE":
      self.oreUsed += quantity
    else:
      qty = self.amounts.get(name, 0)
      if qty < quantity:
        self.request(name, quantity - qty)
      print(f"Withdrawing {quantity} {name}")
      self.amounts[name] = qty - quantity
  def __repr__(self):
    return "\n".join(str(r) for r in self.patterns.values())

def parse(lines):
  proc = Processor()
  pattern = re.compile(r"(\d+)\s([A-Z]+)")
  for line in lines:
    i,o = line.split("=>")
    o = ReactantQuantity(*pattern.search(o).group(2,1))
    i = [ReactantQuantity(*m.group(2,1)) for m in pattern.finditer(i)]
    proc.addRecipe(Recipe(o, *i))
  return proc

inputData = [
  "10 ORE => 10 A",
  "1 ORE => 1 B",
  "7 A, 1 B => 1 C",
  "7 A, 1 C => 1 D",
  "7 A, 1 D => 1 E",
  "7 A, 1 E => 1 FUEL"
]
#inputData = [
#  "9 ORE => 2 A",
#  "8 ORE => 3 B",
#  "7 ORE => 5 C",
#  "3 A, 4 B => 1 AB",
#  "5 B, 7 C => 1 BC",
#  "4 C, 1 A => 1 CA",
#  "2 AB, 3 BC, 4 CA => 1 FUEL"
#]

proc = parse(inputData)
print(proc)
proc.request("FUEL")
print(proc.oreUsed)
