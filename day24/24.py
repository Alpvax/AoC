class Group:
  EID = 0
  GID =  0
  @staticmethod
  def makeID(evil, id = None):
    if id == None:
      if evil:
        id = Group.EID
        Group.EID += 1
      else:
        id = Group.GID
        Group.GID += 1
    return ("Infection " if evil else "Immune ") + str(id)
  def __init__(self, evil, count, hp, atkDmg, atkTyp, init, immune=[], weak=[], id = None):
    self.id = Group.makeID(evil, id)
    self.evil = evil
    self.count = count
    self.hp = hp
    self.atkDmg = atkDmg
    self.atkTyp = atkTyp
    self.init = init
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
  Group(False, 17, 5390, 4507, "fire", 2, weak=["radiation", "bludgeoning"]),
  Group(False, 989, 1274, 25, "slashing", 3, ["fire"], ["bludgeoning", "slashing"]),
]
INFECTION = [
  Group(True, 801, 4706, 116, "bludgeoning", 1, weak=["radiation"]),
  Group(True, 4485, 2961, 12, "slashing", 4, ["radiation"], ["fire", "cold"]),
]

def parseInput(lines):
  import re
  lists = ([], [])
  evil = None
  for line in lines:
    if len(line):
      if re.match("immune system", line, re.I):
        evil = False
      elif re.match("infection", line, re.I):
        evil = True
      else:
        m = re.match(r"(?P<count>\d+) units each with (?P<hp>\d+) hit points(?: \((?P<resist>.+)\))? with an attack that does (?P<atkDmg>\d+) (?P<atkTyp>\w+) damage at initiative (?P<init>\d+)", line)
        if m:
          args = m.groupdict()
          args["evil"] = evil
          if args["resist"]:
            resist = args["resist"]
            for r in re.finditer(r"(?:immune to (?P<immune>\w+(?:, \w+)*))|(?:weak to (?P<weak>\w+(?:, \w+)*))", resist):
              immune, weak = [[t for t in (v if v else "").split(",") if t] for v in r.group("immune", "weak")]
              if immune:
                args["immune"] = immune
              if weak:
                args["weak"] = weak
          del args["resist"]
          group = Group(**args)
          if evil:
            lists[1].append(group)
          else:
            lists[0].append(group)
  return lists


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

if __name__ == "__main__":
  with open("input.txt") as f:
    IMMUNE_SYS, INFECTION = parseInput(f)
  while len(IMMUNE_SYS) > 0 and len(INFECTION) > 1:
    printGroups()
    break#XXX
    target_select()
    attack_targets()
    IMMUNE_SYS, INFECTION = filterGroups()
  printGroups()
  print("Remaining:", max(sum(g.count for g in IMMUNE_SYS), sum(g.count for g in INFECTION)))
