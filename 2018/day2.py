from loadFile import loadfile

def countDups(string):
  c2 = 0
  c3 = 0
  for c in string:
    n = string.count(c)
    if not c2 and n == 2:
      c2 = 1
    if not c3 and n == 3:
      c3 = 1
    if c2 and c3:
      break
  return c2, c3

def matchChars(data):
  for i in range(len(data)):
    a = data[i]
    for j in range(i, len(data)):
      b = data[j]
      errors = 0
      chars = []
      for k in range(len(a)):
        if a[k] == b[k]:
          chars.append(a[k])
        else:
          errors += 1
          if errors > 1:
            break
      if errors == 1:
        return "".join(chars)

if __name__ == "__main__":
  # part 1
  c2 = 0
  c3 = 0
  for line in loadfile(2):
    c = countDups(line)
    c2 += c[0]
    c3 += c[1]
  print(c2 * c3)

  # part 2
  print(matchChars(list(loadfile(2))))
