from functools import reduce
from math import ceil

with open("input_test.txt", "r") as f:
    reactions = {}
    for line in f.readlines():
        reagents, result = line.rstrip().split(" => ")
        quantity, result = result.split(" ")
        quantity = int(quantity)
        rs = [] 
        for r in reagents.split(", "):
            rq, r = r.split(" ")
            rq = int(rq)
            rs.append((rq, r))
        reactions[result] = (quantity, rs)

print(reactions)

def resolve(output, quantity):
    print(f"resolve called for {quantity}x {output}")
    rs = reactions[output][1]
    if len(rs) == 1 and rs[0][1] == "ORE":
        return [(output, quantity)]
    else:
        q = reactions[output][0]
        print(f"made via reactions {rs} in quantity {q}, recursing")
        resolved = []
        for r in rs:
            print(f"working on {r}")
            part = resolve(r[1], r[0])
            print(f"recursively resolved {part}")
            for item in part:
                resolved.append((item[0], ceil(item[1] * quantity / q)))
        print(f"resolved to {resolved}")
        return resolved

def resolve_to_ore(rs):
    def record_material(c, part):
        r, q = part
        c[r] = c[r] + q if r in c else q
        return c
    
    def add_ore_quantity(c, r):
        q, o = reactions[r]
        oq = o[0][0]
        return c + ceil(summed[r] / q) * oq

    summed = reduce(record_material, rs, {})
    print(summed)
    ore = reduce(add_ore_quantity, summed.keys(), 0)
    return ore        

resolved = resolve("FUEL", 1)
print(resolved)
ore = resolve_to_ore(resolved)
print(f"Answer 1: {ore}")