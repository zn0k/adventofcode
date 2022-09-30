import json

with open("input.txt", "r") as f:
    data = json.load(f)

def sum_thing(x, f=None):
    total = 0
    if isinstance(x, int):
        return x
    if isinstance(x, list):
        for i in x:
            total += sum_thing(i, f)
    if isinstance(x, dict):
        if f and f in x.values():
            return total
        for i in x.values():
            total += sum_thing(i, f)
    return total

print(f"Solution 1: {sum_thing(data)}")
print(f"Solution 2: {sum_thing(data, f='red')}")
