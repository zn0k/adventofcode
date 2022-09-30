seed = "1113122113"

def divide(s):
    parts = []
    curr = s[0]
    for c in s[1:]:
        if c == curr[0]:
            curr += c
        else:
            parts.append(curr)
            curr = c
    parts.append(curr)
    return parts

def translate(s):
    return str(len(s)) + s[0]

for x in range(0, 40):
    seed = "".join(map(translate, divide(seed)))

print(f"Solution 1: {len(seed)}")

for x in range(0, 10):
    seed = "".join(map(translate, divide(seed)))

print(f"Solution 2: {len(seed)}")