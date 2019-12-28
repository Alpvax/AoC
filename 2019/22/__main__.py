import collections, os, re

def deal(deck, n = -1):
    if n > 0:
        res = collections.deque()
        for i in range(n):
            res.appendleft(deck.popleft())
    else:
        res = collections.deque(reversed(deck))
        deck.clear()
    return res

def cut(deck, n):
    deck.rotate(-n)
    return deck

def inc(deck, increment):
    i = 0
    l = len(deck)
    table = [None for _ in range(l)]
    while len(deck) > 0:
        table[i] = deck.popleft()
        i = (i + increment) % l
    return collections.deque(table)

def buildDeck(size):
    return collections.deque(range(size))

if False:
    ## Samples:
    d = buildDeck(10)
    d = inc(d, 7)   #deal with increment 7
    d = deal(d)     #deal into new stack
    d = deal(d)     #deal into new stack
    print(d)        #Result: 0 3 6 9 2 5 8 1 4 7

    d = buildDeck(10)
    cut(d, 6)       #cut 6
    d = inc(d, 7)   #deal with increment 7
    d = deal(d)     #deal into new stack
    print(d)        #Result: 3 0 7 4 1 8 5 2 9 6

    d = buildDeck(10)
    d = inc(d, 7)   #deal with increment 7
    d = inc(d, 9)   #deal with increment 9
    cut(d, -2)      #cut -2
    print(d)        #Result: 6 3 0 7 4 1 8 5 2 9

    d = buildDeck(10)
    d = deal(d)     #deal into new stack
    cut(d, -2)      #cut -2
    d = inc(d, 7)   #deal with increment 7
    cut(d, 8)       #cut 8
    cut(d, -4)      #cut -4
    d = inc(d, 7)   #deal with increment 7
    cut(d, 3)       #cut 3
    d = inc(d, 9)   #deal with increment 9
    d = inc(d, 3)   #deal with increment 3
    cut(d, -1)      #cut -1
    print(d)        #Result: 9 2 5 8 1 4 7 0 3 6
else:
    def cutC(num):
        def wrapped(deck):
            return cut(deck, num)
        return wrapped
    
    def incC(num):
        def wrapped(deck):
            return inc(deck, num)
        return wrapped

    ops = {
        "stack": lambda m: deal,
        "cut (-?\d+)": lambda m: cutC(m[1]),
        "increment (-?\d+)": lambda m: cutC(m[1]),
    }

    deck = buildDeck(10007)
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        for line in file:
            m = re.search(r"(stack)|cut (-?\d+)|increment (-?\d+)")
            if m.group(1):
                deck = deal(deck)
            elif m.group(2):
                deck = cut(deck, int(m.group(2)))
            elif m.group(3):
                deck = inc(deck, int(m.group(3)))
    print(deck)