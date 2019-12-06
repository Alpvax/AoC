#! /bin/python3

if True:
  with open("input.txt") as f:
    inputData = [int(n) for n in f.read().split(",")]
#inputData = [1,9,10,3,2,3,11,0,99,30,40,50]
#inputData = [1002,4,3,4,33]
#inputData = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
#inputData = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]

operations = { # (numArgs, (args, currentIndex) -> (result, newIndex))
  1: (2, lambda args, i: (sum(args), i + 4)),                               # 1 - Sum
  2: (2, lambda args, i: (args[0] * args[1], i + 4)),                       # 2 - Product
  3: (0, lambda args, i: (int(input("Enter the input number: ")), i + 2)),  # 3 - Input
  4: (1, lambda args, i: (print("Output:", args[0]), i + 2)),               # 4 - Output
  5: (2, lambda args, i: (None, (i + 3) if not args[0] else args[1])),      # 5 - JumpIfTrue
  6: (2, lambda args, i: (None, (i + 3) if args[0] else args[1])),          # 6 - JumpIfFalse
  7: (2, lambda args, i: (1 if args[0] < args[1] else 0, i + 4)),           # 7 - LessThan
  8: (2, lambda args, i: (1 if args[0] == args[1] else 0, i + 4)),          # 8 - Equals
}

def getValue(iData, index, immediate):
  data = iData[index]
  if immediate:
    return data
  return iData[data]

def run():
  iData = inputData.copy()
  i = 0
  #print([n for n in range(len(iData))])
  while i < len(iData):
    #print(iData)
    code = iData[i]
    op = code % 100
    immediate = "{:03d}".format((code // 100))
    if op == 99:
      break
    else:
      #print(i, code)
      numArgs,oper = operations.get(op, (0, lambda args, index: (_ for _ in ()).throw(Exception("Invalid op at index {} ({})".format(i, code)))))
      args = [getValue(iData, i+j+1, immediate[-1 - j] == "1") for j in range(numArgs)]
      #print(i, op, args)
      res, nextI = oper(args, i)
      if res != None:
        iData[iData[i + numArgs + 1]] = res
        #i += 1
        #print("iData[{} -> {}] = {}".format(i + numArgs + 1, iData[i + numArgs + 1], res))
      #i += numArgs + 1
      i = nextI
  return iData[0]

run()
