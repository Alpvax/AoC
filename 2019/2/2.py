#! /bin/python3

with open("input.txt") as f:
  inputData = [int(n) for n in f.read().split(",")]
#inputData = [1,9,10,3,2,3,11,0,99,30,40,50]

operations = {
  1: lambda a,b: a+b,
  2: lambda a,b: a*b,
}

def run(noun=12, verb=2):
  iData = inputData.copy()
  iData[1] = noun
  iData[2] = verb
  for i in range(0, len(iData), 4):
    op = iData[i]
    if op == 99:
      break
    else:
      oper = operations.get(op, "ERROR: Invalid op (" + str(i) + ")")
      a = iData[iData[i+1]]
      b = iData[iData[i+2]]
      iData[iData[i+3]] = oper(a, b)
  return iData[0]
  
for n in range(100):
  for v in range(100):
    res = run(n,v)
    if n==12 and v==2:
      print("2.1:", res)
    if res == 19690720:
      print("2.2: {:02}{:02}".format(n,v))