with open("input_test.txt", "r") as f:
    line = f.readlines()[0].rstrip()
    signal = [int(c) for c in line]

signal *= 10000

def calc_patterns(l):
    size = len(l)
    for i in range(0, size):
        j = i + 1
        pattern = [0] * j + [1] * j + [0] * j + [-1] * j
        while len(pattern) < size: pattern += pattern
        patterns[i] = pattern[1::]

def calc_element(l, i):
    out = sum(map(lambda x: x[0] * x[1], zip(l, patterns[i])))
    return int(str(out)[-1])

def calc_step(l):
    return list(map(lambda x: calc_element(l, x), range(0, len(l))))

patterns = {}
calc_patterns(signal)
for _ in range(100):
    signal = calc_step(signal)

offset = int("".join(map(lambda x: str(x), signal[0:7])))
answer = "".join(map(lambda x: str(x), signal[offset:offset + 8]))
print(f"Answer 1: {answer}")