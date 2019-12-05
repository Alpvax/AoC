#! /bin/python3

#with open("input.txt") as f:
#  inputData = [int(n) for n in f.read().split(",")]
#inputData = [1,9,10,3,2,3,11,0,99,30,40,50]
inputData = [1002,4,3,4,33]

operations = {
  1: (2, lambda args: sum(args)),
  2: (2, lambda args: args[0] * args[1]),
  3: (1, lambda args: args[0]),
}

def getValue(iData, index, immediate):
  print(index, "->", iData[index], immediate)
  return iData[index] if immediate else iData[iData[index]]

def run(inputArg):
  iData = inputData.copy()
  iData[1] = inputArg
  i = 0
  while i < len(iData):
    code = iData[i]
    op = code % 100
    immediate = "{:03d}".format((code // 100))
    print(immediate, [(j, immediate[-1 -j]) for j in range(3)])
    print()
    if op == 99:
      break
    else:
      print(op, operations.get(op, "ERROR: Invalid op (" + str(i) + ")"))
      numArgs,oper = operations.get(op, "ERROR: Invalid op (" + str(i) + ")")
      args = [getValue(iData, i+j, immediate[-1 - j] == "1") for j in range(numArgs)]
      iData[iData[i + numArgs + 1]] = oper(args)
      i += numArgs + 2
  return iData[0]

print(run(1))
