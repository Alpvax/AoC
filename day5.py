from loadFile import loadfile

a = ord("a")
A = ord("A")

def reactedLength(data):
  last = None
  while last != data:
    last = data
    for i in range(26):
      data = data.replace(chr(a + i) + chr(A + i),"")
      data = data.replace(chr(A + i) + chr(a + i),"")
  return len(data)

if __name__ == "__main__":
  data = list(loadfile(5))[0] # Strip newline character :@

  print(reactedLength(data))

  best = len(data)
  for i in range(26):
     best = min(best, reactedLength(data.replace(chr(a + i), "").replace(chr(A + i), "")))
  print(best)
