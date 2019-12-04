from loadFile import loopData

if __name__ == "__main__":
  total = 0
  totals = set()
  def onLoop(loopnum):
    if loopnum == 1:
      print(total)
  for line in loopData(1, onLoop):
    total += int(line)
    if total in totals:
      print(total)
      break
    totals.add(total)
