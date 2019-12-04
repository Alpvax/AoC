from collections import deque, Counter

def printRow(marbles, current, player, pad = 2):
  def fmt(marble, index):
    return (" " * pad + ("({})" if index == current else " {} ").format(marble))[-pad-2:]
  print("[{}] {}".format(player, "".join([fmt(m, i) for i,m in enumerate(marbles)])))

if __name__ == "__main__":
  numPlayers = 416
  maxMarble = 7161700

  scores = Counter()
  marbles = deque([0])
#  printRow(marbles, current.index, "-")
  for i in range(1, maxMarble + 1):
    if i % 23 == 0:
      marbles.rotate(7)
      scores[i % numPlayers] += marbles.pop() + i
      marbles.rotate(-1)
    else:
      marbles.rotate(-1)
      marbles.append(i)

print(scores.most_common()[0][1])
