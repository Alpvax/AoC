import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, "../intcode")

import intcode

machine = intcode.IntCodeMachine()
