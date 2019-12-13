import inspect, collections

def parameterMode(code):
  def wrap(func):
    parameterModes[code] = func
    return func
  return wrap

parameterModes = {}
@parameterMode(0)
def positionMode(machine, index):
  return machine.getRaw(index)
@parameterMode(1)
def immediateMode(machine, index):
  return index
@parameterMode(2)
def relativeMode(machine, index):
  return machine.getRaw(index) + machine.relativeIndex

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
      args = [machine.getRaw(getPMode(fullCode, n)(machine, ai + n)) for n in range(self.numParams)]
      kwargs = {k:v for k,v in dict(machine=machine, i = ai - 1, store = machine.store, jumpTo = setIndex).items() if k in self._sig.parameters}
      if machine.debug & 2: # debug bitwise flags
        print(
          "Args for", str(self), "@ index", ai - 1, "code =", fullCode, "->",
          list(zip((fullCode // 10**(n + 2) % 10 for n in range(self.numParams)), args)),
          kwargs
        )
      res = opFunc(*args, **kwargs)
      if res != None:
        machine.store(getPMode(fullCode, self.numParams)(machine, nextIndex), res)
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
  machine.stop(True)
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
  if machine.debug & 1:
    print("Output:", a)
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

class IntCodeMachine:
  def __init__(self, initialState, debug = 0, name = "IntCodeMachine"):
    self.name = name
    self.debug = debug
    if debug & 1:
      print("Initialising IntCode machine with operators:\n", sorted(str(op).replace("Op", "", 1) for op in IntCodeOperator.operators.values()))
    self._initialState = initialState
    self._in = collections.deque()
    self._out = collections.deque()
    self.reset()
  def getRaw(self, index):
    return self.data.get(index, 0)
  def store(self, pos, value):
    self.data[pos] = value
  @property
  def completed(self):
    return self.__completed
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
  def hasOutput(self):
    return len(self._out) > 0
  def setOutput(self, val):
    self._out.append(val)
  def clearIO(self):
    self._in.clear()
    self._out.clear()
  def reset(self):
    self.clearIO()
    self.__completed = False
    self.currentIndex = 0
    self.relativeIndex = 0
    self.data = {i: n for i,n in enumerate(self._initialState)}
    d = self.debug
    self.debug = 0
    self.stop()
    self.debug = d
  def start(self, *inputs):
    if self.debug & 1:
      print("Starting machine:", self.name)
    if inputs:
      self.setInputs(*inputs)
    self.__running = True
    while self.__running and self.currentIndex <= max(self.data.keys()) and not self.completed:
      code = self.getRaw(self.currentIndex)
      op = IntCodeOperator.parse(code)
      op(self, code)
      #print(self.currentIndex, op.icodeOp, inspect.signature(op).parameters)
      #print("Result:", res)
  def stop(self, completed = False):
    if self.debug & 1:
      print("Stopping machine: {} ({}completed)".format(self.name, "" if completed else "not "))
    self.__running = False
    self.__completed = completed
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
