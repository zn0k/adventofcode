lower = 137683
upper = 596253

def check(x):
    x = str(x)
    tuples = list(zip(x, x[1::]))
    adjacent = list(filter(lambda x: x[0] == x[1], tuples))
    if len(adjacent):
        increasing = list(filter(lambda x: x[0] <= x[1], tuples))
        if len(increasing) == len(x) - 1:
            return True
    return False

candidates = list(filter(check, range(lower, upper + 1)))
print(f"Answer 1: {len(candidates)}")

def check2(x):
    x = str(x)
    tuples = list(zip(x, x[1::]))
    adjacent = set(map("".join, filter(lambda x: x[0] == x[1], tuples)))
    for a in adjacent:
        start = 0
        while True:
            start = x.find(a, start)
            if start == -1: break
            if start == 0: 
                if x[2] != a[0]: return True
            else:
                if x[start - 1] != a[0]:
                    if start + 2 < len(x):
                        if x[start + 2] != a[0]: return True
                    else:
                        return True
            start += 1
    return False
            
candidates = list(filter(check2, candidates))
print(f"Answer 2: {len(candidates)}")