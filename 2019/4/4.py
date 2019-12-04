import re


r = [138241,674034]
count1 = 0
count2 = 0
for i in range (1,10):
  for j in range(i,10):
    for k in range(j,10):
      for l in range(k,10):
        for m in range(l,10):
          for n in range(m,10):
            if \
              i == j or \
              j == k or \
              k == l or \
              l == m or \
              m == n:
              code = i*100000 + j*10000 + k*1000 + l*100 + m*10 + n
              if r[0] <= code <= r[1]:
                count1 += 1
                for f in re.finditer(r"(\d)\1+", str(code)):
                  if len(f[0]) == 2:
                    print(f[0])
                    count2 += 1
                    break
print(count1)
print(count2)