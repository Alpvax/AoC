import os, collections, itertools
from .. import intcode

if True:
  with open(os.path.dirname(__file__) + "/input.txt") as f:
    inputData = [int(n) for n in f.read().split(",")]
else:
  #inputData = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
  inputData = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

@intcode.IntCodeOperator(4)
def boosterOutputOp(a, machine):
  machine.setOutput(a)
  machine.stop()

machines = collections.deque(intcode.IntCodeMachine(inputData, debug=0) for i in range(5)) # All machines identical, debug general

def runAmpLoop(inputs):
  for i in range(5): # reset all machines (order irrelevant) and set phase
    m = machines[0]
    m.reset()
    m.name = "abcde"[i]
    m.setInputs(inputs[i])
    machines.rotate()
  res = 0 # Start first machine with 0
  while len([m for m in machines if not m.completed]) > 0:
    m = machines[0]
    m.start(res)
    machines.rotate()
    if m.hasOutput():
      res = m.output
  return res

print(max(runAmpLoop(inputs) for inputs in itertools.permutations(range(5, 10))))
