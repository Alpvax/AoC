#! /bin/python3
import itertools, collections

if True:
  with open("input.txt") as f:
    inputData = [int(n) for n in f.read().split(",")]
#inputData = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
#inputData = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]

class IO:
  def __init__(self, inputs=[]):
    self._in = collections.deque(inputs)
    self._out = collections.deque()
  @property
  def input(self):
    if len(self._in) > 0:
      return self._in.popleft()
    return int(input("Enter the input number: "))
  def setInputs(self, *vals):
    for val in vals:
      self._in.append(val)
  @property
  def output(self):
    return self._out.popleft()
  def setOutput(self, val):
    self._out.append(val)
    #return val
  def clear(self):
    self._in.clear()
    self._out.clear()

ioManager = IO()

operations = { # (numArgs, (args, currentIndex) -> (result, newIndex))
  1: (2, lambda args, i: (sum(args), i + 4)),                                     # 1 - Sum
  2: (2, lambda args, i: (args[0] * args[1], i + 4)),                             # 2 - Product
  #3: (0, lambda args, i: (int(input("Enter the input number: ")), i + 2)),       # 3 - Input (manual)
  3: (0, lambda args, i: (ioManager.input, i + 2)),                               # 3 - Input (automatic)
  #4: (1, lambda args, i: (print("Output:", ioManager.setOutput(args[0])), i + 2)),# 4 - Output
  4: (1, lambda args, i: (ioManager.setOutput(args[0]), i + 2)),                  # 4 - Output (no print)
  5: (2, lambda args, i: (None, (i + 3) if not args[0] else args[1])),            # 5 - JumpIfTrue
  6: (2, lambda args, i: (None, (i + 3) if args[0] else args[1])),                # 6 - JumpIfFalse
  7: (2, lambda args, i: (1 if args[0] < args[1] else 0, i + 4)),                 # 7 - LessThan
  8: (2, lambda args, i: (1 if args[0] == args[1] else 0, i + 4)),                # 8 - Equals
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

def runAmpLoop(inputs):
  ioManager.clear() # Ensure no errors from previous run
  ioManager.setOutput(0) #For use in first loop
  for i in inputs:
    ioManager.setInputs(i, ioManager.output)
    run()
  return ioManager.output

print(max(runAmpLoop(inputs) for inputs in itertools.permutations(range(5))))
