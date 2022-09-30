with open("input.txt", "r") as f:
    presents = [list(map(lambda y: int(y), x.rstrip().split("x"))) for x in f.readlines()]

total = 0
for p in presents:
    s1 = p[0] * p[1]
    s2 = p[1] * p[2]
    s3 = p[0] * p[2]
    slack = min([s1, s2, s3])
    total += 2 * s1 + 2 * s2 + 2 * s3 + slack

print(f"Solution 1: {total}")

total = 0
for p in presents:
    p1 = 2 * p[0] + 2 * p[1]
    p2 = 2 * p[1] + 2 * p[2]
    p3 = 2 * p[0] + 2 * p[2]
    bow = p[0] * p[1] * p[2]
    total += min([p1, p2, p3]) + bow

print(f"Solution 2: {total}")