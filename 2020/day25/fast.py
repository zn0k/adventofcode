p = 8458505
q = 16050997

n = 20201227
r = 7

s = int(p ** 0.5)
print(s)
d = {pow(r, j, n): j for j in range(s+1)}
#print(d)
f = pow(r, s * (n - 2), n)
t = p
i = 0

while t not in d.keys():
    i += 1
    t = (t * f) % n

print(pow(q, i * s + d[t], n))