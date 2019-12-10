import inspect, collections

parameterModes = {
  0: lambda m, i: m.data[m.data[i]],
  1: lambda m, i: m.data[i],
  2: lambda m, i: m.data[m.relativeIndex + i],
}
def getPMode(code, pnum):
  return parameterModes.get(code // 10**(pnum + 2) % 10, parameterModes[0])

class IntCodeOperator:
  operators = {}
  @staticmethod
  def parse(code):
    op = IntCodeOperator.operators.get(code % 100)
    if not op:
      raise Exception("Invalid operator with code " + str(code % 100))
    return op._func
  def __init__(self, code):
    self.code = code
    IntCodeOperator.operators[self.code] = self
  def __call__(self, opFunc):
    self.name = opFunc.__name__
    self._sig = inspect.signature(opFunc)
    self.numParams = len([p for p in self._sig.parameters if p not in ["machine", "i", "store", "jumpTo"]])
    def wrapped_func(machine, fullCode):
      nextIndex = machine.currentIndex + self.numParams + 1
      def setIndex(i):
        nonlocal nextIndex
        nextIndex = i
      ai = machine.currentIndex + 1
      args = [getPMode(fullCode, n)(machine, ai + n) for n in range(self.numParams)]
      kwargs = {k:v for k,v in dict(machine=machine, i = ai - 1, store = machine.store, jumpTo = setIndex).items() if k in self._sig.parameters}
      #print("Args for op", self.code, "@ index", ai - 1, "->", args, kwargs)
      res = opFunc(*args, **kwargs)
      if res != None:
        machine.store(machine.get(nextIndex), res)
        nextIndex += 1
      machine.currentIndex = nextIndex
      return res
    self._func = wrapped_func
    wrapped_func.__name__ = opFunc.__name__ + " (wrapped)"
    wrapped_func.__str__ = lambda: "IntCode {} ({})".format(self.code, self.name)
    wrapped_func.icodeOp = self
    return wrapped_func
  def __str__(self):
    return "IntCode {} ({})".format(self.code, self.name)


@IntCodeOperator(99)
def end_program(machine):
  machine.stop()
  #print("Ended")

@IntCodeOperator(1)
def addOp(a, b):
  return a + b
@IntCodeOperator(2)
def multOp(a, b, store):
  return a * b
@IntCodeOperator(3)
def inputOp(machine):
  return machine.input
@IntCodeOperator(4)
def outputOp(a, machine):
  #print("Output:", a)
  machine.setOutput(a)
@IntCodeOperator(5)
def trueJumpOp(a, b, jumpTo):
  if a:
    jumpTo(b)
@IntCodeOperator(6)
def falseJumpOp(a, b, jumpTo):
  if not a:
    jumpTo(b)
@IntCodeOperator(7)
def lessThanOp(a, b):
  return 1 if a < b else 0
@IntCodeOperator(8)
def equalsOp(a, b):
  return 1 if a == b else 0
@IntCodeOperator(9)
def setRelIndexOp(a, machine):
  machine.relativeIndex += a

#class IntCodeOperator:
#  operators = {
#    99: IntCodeOperator(99, lambda: "STOP", storeResult=False),
#    1
#  }
#  @staticmethod
#  def parse(code):
#    op = IntCodeOperator.operators.get(code % 100)
#    if not op:
#      raise Exception("Invalid operator with code " + str(code % 100))
#    return op
#  def __init__(self, code, function, storeResult = True):
#    self.code = code
#    params = inspect.signature(function).parameters
#    self._numParams = len(p for p in params if p.name not in ["m", "i"])
#    self.store = storeResult
#    self._function = function
#    IntCodeOperator.operators[code] = self
#  def operate(self, machine):
#    next()

class IntCodeMachine:
  def __init__(self, initialState):
    #print("Initialising IntCode machine with operators:\n", sorted(str(op).replace("Op", "", 1) for op in IntCodeOperator.operators.values()))
    self._initialState = initialState
    self._in = collections.deque()
    self._out = collections.deque()
    self.relativeIndex = 0
    self.currentIndex = 0
    self.data = initialState.copy()
  def get(self, index):
    return self.data[index]
  def store(self, pos, value):
    self.data[pos] = value
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
  def clearIO(self):
    self._in.clear()
    self._out.clear()
  def reset(self):
    self.clearIO()
    self.currentIndex = 0
    self.relativeIndex = 0
    self.data = self._initialState.copy()
    self.stop()
  def start(self, *inputs):
    if inputs:
      self.setInputs(*inputs)
    self.__running = True
    while self.__running and self.currentIndex < len(self.data):
      code = self.get(self.currentIndex)
      op = IntCodeOperator.parse(code)
      res = op(self, code)
      #print(self.currentIndex, op.icodeOp, inspect.signature(op).parameters)
      #print("Result:", res)
  def stop(self):
    self.__running = False
  def __iter__(self):
    return self
  def __next__(self):
    num = self.data[self.currentIndex]
    self.currentIndex += 1
    return num

if __name__=="__main__":
  machine = IntCodeMachine([3,3,1105,-1,9,1101,0,0,12,4,12,99,1])
  machine.start()
  print(machine.output)
