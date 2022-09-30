import hashlib

secret = "iwrupvqb"

x = 0
while True:
    s = secret + str(x)
    h = hashlib.md5(s.encode()).hexdigest()
    if h.startswith("00000"):
        break
    x += 1

print(f"Solution 1: {x}")

x = 0
while True:
    s = secret + str(x)
    h = hashlib.md5(s.encode()).hexdigest()
    if h.startswith("000000"):
        break
    x += 1

print(f"Solution 2: {x}")