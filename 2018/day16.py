from loadFile import loadfile
from singleton import Meta
import re

class Operation(metaclass = Meta):
  __funcs = {
    "add": lambda a, b: a + b,
    "mult": lambda a, b: a * b,
    "ban": lambda a, b: a & b,
    "bor": lambda a, b: a | b,
    "assign": lambda a, b: a,
    "gtr": lambda a, b: int(a > b),
    "equ": lambda a, b: int(a == b),
  }
  def __init__(self, name, opfunc, b="r", a="r"):
    self.name = name
    self.opcode = -1
    self.opfunc = opfunc if callable(opfunc) else Operation.__funcs[opfunc]
    self.bRef = b and b != "v"
    self.aRef = a and a != "v"
  def apply(self, registers, a, b, c):
    a = registers[a] if self.aRef else a
    b = registers[b] if self.bRef else b
    registers[c] = self.opfunc(a, b)
    return registers

funcs = {
  # Addition:
  "addr": Operation ("addr", "add"), # (add register) stores into register C the result of adding register A and register B.
  "addi": Operation ("addi", "add", b="v"), #  (add immediate) stores into register C the result of adding register A and value B.
  # Multiplication:
  "mulr": Operation ("mulr", "mult"), # (multiply register) stores into register C the result of multiplying register A and register B.
  "muli": Operation ("muli", "mult", b="v"), # (multiply immediate) stores into register C the result of multiplying register A and value B.
  # Bitwise AND:
  "banr": Operation ("banr", "ban"), # (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
  "bani": Operation ("bani", "ban", b="v"), # (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
  # Bitwise OR:
  "borr": Operation ("borr", "bor"), # (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
  "bori": Operation ("bori", "bor", b="v"), # (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
  # Assignment:
  "setr": Operation ("setr", "assign", b=False), # (set register) copies the contents of register A into register C. (Input B is ignored.)
  "seti": Operation ("seti", "assign", b=False, a="v"), # (set immediate) stores value A into register C. (Input B is ignored.)
  # Greater-than testing:
  "gtir": Operation ("gtir", "gtr", a="v"), # (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
  "gtri": Operation ("gtri", "gtr", b="v"), # (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
  "gtrr": Operation ("gtrr", "gtr"), # (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
  # Equality testing:
  "eqir": Operation ("eqir", "equ", a="v"), # (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
  "eqri": Operation ("eqri", "equ", b="v"), # (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
  "eqrr": Operation ("eqrr", "equ") # (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
}

class Sample():
  def __init__(self, before):
    self.before = before
  def setOp(self, ops):
    self.opNum = ops[0]
    self.ops = ops[1:]
  def setAfter(self, after):
    self.after = after
    self.valid = {o for o in funcs.values() if o.apply(self.before.copy(), *self.ops) == self.after}
    #if len(self.valid) == 1:
    #  list(self.valid)[0].opcode = self.opNum

if __name__ == "__main__":
  opcodes = {}
  samples = []
  current = None
  begin = re.compile(r"Before:\s+\[(.+)\]")
  end = re.compile(r"After:\s+\[(.+)\]")
  empty = 0
  registers = [0] * 4
  for line in loadfile(16):
    if empty == 3:
      empty += 1 # Force next step
      for n, ops in opcodes.items():
        o = {op for op in ops if op.opcode < 0}
        if len(o) == 1:
          o.pop().opcode = n
      opcodes = {o.opcode: o for o in funcs.values()}
    elif empty > 3:
      proc = [int(i) for i in line.split(" ")]
      print(proc)
      registers = opcodes[proc[0]].apply(registers, *proc[1:])
    else:
      if len(line) < 1:
        empty += 1
        continue
      else:
        empty = 0
      b = begin.match(line)
      e = end.match(line)
      if current:
        if e:
          current.setAfter([int(i) for i in e[1].split(",")])
          num = current.opNum
          valid = {o for o in current.valid if o.opcode < 0}
          current = None
          if num in opcodes:
            opcodes[num] = opcodes[num] & valid
          else:
            opcodes[num] = valid
          if len(opcodes[num]) == 1:
            list(opcodes[num])[0].opcode = num
        elif len(line) > 0:
          current.setOp([int(i) for i in line.split(" ")])
      elif b:
        current = Sample([int(i) for i in b[1].split(",")])
        samples.append(current)
  print(len([s for s in samples if len(s.valid) >= 3]))

  print(registers)
