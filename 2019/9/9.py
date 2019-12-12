from .. import intcode
import os

#inputData = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99] # takes no input and produces a copy of itself as output.
#inputData = [1102,34915192,34915192,7,4,7,99,0] # should output a 16-digit number.
#inputData = [104,1125899906842624,99] # should output the large number in the middle.
with open(os.path.dirname(__file__) + "/input.txt") as f:
  inputData = [int(n) for n in f.read().split(",")]

machine = intcode.IntCodeMachine(inputData, False)
machine.start(1)
print(machine.output)
machine.reset()
machine.start(2)
print(machine.output)
