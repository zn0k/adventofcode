with open("input.txt", "r") as f:
    lines = [x.rstrip() for x in f.readlines()]

codes = list(map(lambda x: len(x), lines))
codelen = sum(codes)
mems = list(map(lambda x: len(x.encode("utf-8").decode("unicode_escape")) - 2, lines))
memlen = sum(mems)

print(f"Solution 1: {codelen - memlen}")

escaped = list(map(lambda x: len(x.replace('\\', '\\\\').replace('"', '\\"')) + 2, lines))
escapedlen = sum(escaped)

print(f"Solution 2: {escapedlen - codelen}")