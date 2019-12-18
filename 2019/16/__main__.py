import itertools

def makePattern(index, length, base=[0,1,0,-1]):
  nbase = (n for n in base for _ in range(index + 1))
  #print(list(nbase))
  res = itertools.cycle(nbase)
  next(res)
  return [next(res) for _ in range(length)]

def processDigit(numStr, pattern):
  res = 0
  #print(f"Processing {numStr} with pattern {pattern}")
  for i in range(len(numStr)):
    d = int(numStr[i]) * pattern[i]
    #print(res, end="")
    res += d
    #print(f" += {d} = {res}")
  #print(f"=> {abs(res) % 10}")
  return abs(res) % 10

def process(signal, offset = 0):
  l = len(signal)
  patterns = tuple(makePattern(i, l) for i in range(l))
  for i in range(100):
    signal = "".join(str(processDigit(signal, p)) for p in patterns)
  print(f"After {i + 1} phases: [{offset}:{offset+8}] = {signal[offset:offset + 8]}")

if False:
  inputSignal = "59709275180991144553584971145772909665510077889137728108418335914621187722143499835763391833539113913245874471724316543318206687063884235599476032241946131415288903315838365933464260961288979081653450180693829228376307468452214424448363604272171578101049695177870848804768766855959460302410160410252817677019061157656381257631671141130695064999297225192441065878259341014746742840736304437968599872885714729499069286593698777113907879332554209736653679474028316464493192062972874319626623316763537266681767610340623614648701699868901159785995894014509520642548386447251984766543776759949169049134947575625384064448900019906754502662096668908517457172"
else:
  #inputSignal = "12345678" # After 4 becomes 29029498
  inputSignal = "80871224585914546619083218645595" # After 100 becomes 24176176.
  #inputSignal = "19617804207202209144916044189917" # After 100 becomes 73745418.
  #inputSignal = "69317163492948606335995924319873" # After 100 becomes 52432133

process(inputSignal)
process(inputSignal * 10000, int(inputSignal[0:7]))
