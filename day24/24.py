class Group:
  def __init__(self, id, evil, count, hp, atkDmg, atkTyp, initiative, immune=[], weak=[]):
    self.id = ("Infection " if evil else "Immune ") + str(id)
    self.evil = evil
    self.count = count
    self.hp = hp
    self.atkDmg = atkDmg
    self.atkTyp = atkTyp
    self.init = initiative
    self.immune = immune
    self.weak = weak
    self._target = None
    self.targetted = False
  @property
  def target(self):
    return self._target
  @target.setter
  def target(self, t):
    if t:
      t.targetted = True
    elif self._target:
      self._target.targetted = False
    self._target = t
  @property
  def good(self):
    return not self.evil
  @property
  def power(self):
    return self.count * self.atkDmg
  @property
  def dead(self):
    return self.count < 1
  def getModifiedDamage(self, amount, dType):
    if dType in self.immune:
      return 0
    return amount * 2 if dType in self.weak else amount
  def damage(self, amount):
    "pass in modified damage. returns number of units killed"
    if amount <= 0:
      return 0
    killed = min(self.count, amount // self.hp)
    self.count -= killed
    return killed
  def __lt__(self, other):
    if self.power == other.power:
      return self.init < other.init
    return self.power < other.power
  def __str__(self):
    return "{0} units each with {1} hit points {5} with an attack that does {2} {3} damage at initiative {4}".format(
      self.count,
      self.hp,
      self.atkDmg,
      self.atkTyp,
      self.init,
      "(" + "; ".join(s for s in [
        "immune to " + ", ".join(self.immune) if self.immune else None,
        "weak to " + ", ".join(self.weak) if self.weak else None
      ] if s) + ")"
    )
      
IMMUNE_SYS = [
  Group(1, False, 17, 5390, 4507, "fire", 2, weak=["radiation", "bludgeoning"]),
  Group(2, False, 989, 1274, 25, "slashing", 3, ["fire"], ["bludgeoning", "slashing"]),
]
INFECTION = [
  Group(1, True, 801, 4706, 116, "bludgeoning", 1, weak=["radiation"]),
  Group(2, True, 4485, 2961, 12, "slashing", 4, ["radiation"], ["fire", "cold"]),
]

def printGroups():
  print("Immune system:")
  if len(IMMUNE_SYS) < 1:
    print("No groups remain")
  for g in IMMUNE_SYS:
    print(" ", g.id, "contains", g.count, "units")
  print("Infection:")
  if len(INFECTION) < 1:
    print("No groups remain")
  for g in INFECTION:
    print(" ", g.id, "contains", g.count, "units")

def target_select():
  groups = sorted(INFECTION + IMMUNE_SYS, reverse=True)#, key = lambda g: g.power)
  for group in groups:
    targets = [t for t in (IMMUNE_SYS if group.evil else INFECTION) if not t.targetted]
    if len(targets) > 0:
      target = max((
        target.getModifiedDamage(group.power, group.atkTyp),
        target.power,
        target.init,
        i
      ) for i, target in enumerate(targets))
      group.target = targets[target[-1]]
      print(group.id, "will attack", group.target.id, "for", target[0], "damage.")
    
def attack_targets():
  groups = sorted(INFECTION + IMMUNE_SYS, reverse=True, key = lambda g: g.init)
  for group in groups:
    if group.target:
      print(group.id, "attacks", group.target.id, "killing", group.target.damage(group.target.getModifiedDamage(group.power, group.atkTyp)), "units.")
    
def filterGroups():
  good = []
  evil = []
  for g in IMMUNE_SYS:
    if not g.dead:
      g.target = None
      good.append(g)
  for g in INFECTION:
    if not g.dead:
      g.target = None
      evil.append(g)
  return good, evil
    
while len(IMMUNE_SYS) > 0 and len(INFECTION) > 1:
  printGroups()
  target_select()
  attack_targets()
  IMMUNE_SYS, INFECTION = filterGroups()
printGroups()
print("Remaining:", max(sum(g.count for g in IMMUNE_SYS), sum(g.count for g in INFECTION)))