from loadFile import loadfile
import re
from collections import Counter

class GuardMeta(type):
  def __call__(cls, id, *args, **kwarg):
    if id in cls.ids:
      return cls.ids[id]
    g = super().__call__(id, *args, **kwarg)
    cls.ids[id] = g
    return g

class Guard(metaclass=GuardMeta):
  ids = {}
  def __init__(self, id):
    self.id = id
    self.days = {}
    self.day = None
    self.sleepStart = None
    self.allMins = Counter()

  def setDay(self, day):
    self.day = day
    self.days[day] = set()
  def sleep(self, time):
    self.sleepStart = time
  def wake(self, time):
    for m in range(self.sleepStart, time):
      self.days[self.day].add(m)
      self.allMins[m] += 1
  def sleepAmount(self):
    total = 0
    for s in self.days.values():
      total += len(s)
    return total
  def mostCommonMin(self):
    if len(self.allMins) < 1:
      return 0,0
    return self.allMins.most_common(1)[0]



if __name__ == "__main__":
  pattern =  re.compile(r"\[1518-(?P<day>\d+-\d+)\s\d+:(?P<min>\d+)\]\s(?:(?:Guard #(?P<gid>\d+) begins shift)|falls a(?P<sleep>sleep)|(?P<wake>wake)s up)")
  regions = []
  guard = None
  for line in sorted(loadfile(4)):
    m = pattern.match(line)
    gid = m.group("gid")
    sleep = bool(m.group("sleep"))
    wake = bool(m.group("wake"))
    if gid:
      guard = Guard(gid)
    elif guard:
      guard.setDay(m.group("day"))
      minute = int(m.group("min"))
      if sleep:
        guard.sleep(minute)
      elif wake:
        guard.wake(minute)
  g = sorted(Guard.ids.values(), key=lambda g: g.sleepAmount(), reverse=True)[0]
  print("Guard {} slept for {} min(s) total. Most slept minute: {}".format(g.id, g.sleepAmount(), g.mostCommonMin()[0]))
  print(int(g.id) * g.mostCommonMin()[0])
  g = sorted(Guard.ids.values(), key=lambda g: g.mostCommonMin()[1], reverse=True)[0]
  print("Guard {} slept for {} min(s) total. Most slept minute: {}".format(g.id, g.sleepAmount(), g.mostCommonMin()))
  print(int(g.id) * g.mostCommonMin()[0])
