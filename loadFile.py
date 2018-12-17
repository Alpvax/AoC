def getFname(num, sample=False):
  fname = ""
  try:
    num = int(num)
    fname = "day" + str(num) + ("Sample" if sample else "") + "Data.txt"
  except ValueError:
    fname = num
  return fname

data = {}

def loadfile(num, sample=False):
  fname = getFname(num, sample)
  if fname in data:
    return iter(data[fname])
  else:
    with open(fname, "r") as file:
      for line in file:
        yield line.rstrip("\n")

def loopData(num, onLoop=lambda n: True):
  loopnum = 0
  while True:
    yield from loadfile(num)
    loopnum += 1
    if onLoop(loopnum) == False: # Must return False to break, other falsey values (e.g. None) will continue
      break
