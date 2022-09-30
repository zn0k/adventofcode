from itertools import combinations

with open("input.txt", "r") as f:
    lines = list(map(lambda x: int(x), f.read().split("\n")))

keys = lines[0:25]
nums = lines[25::]

def sum_tup(t):
    return 0 if t[0] == t[1] else t[0] + t[1]

def check_num(keys, num):
    return num in list(map(sum_tup, combinations(keys, 2)))

for i in nums:
    if not check_num(keys, i):
        vuln = i
        break
    keys = keys[1::] + [i]

print(f"Vulnerable value: {vuln}")

def find_weakness(lines):
    for i in range(0, len(lines)):
        for j in range(i + 1, len(lines)):
            if sum(lines[i:j]) == vuln:
                return min(lines[i:j]) + max(lines[i:j])

weakness = find_weakness(lines)
print(f"Weakness: {weakness}")

#Answer 1: 35085495345032
#Answer 2: 3500556055354