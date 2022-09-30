import itertools

with open("input.txt", "r") as f:
    ops = [line.rstrip() for line in f.readlines()]

def apply_mask(mask, val):
    val = int(mask.replace("X", "0"), 2) | val
    return int(mask.replace("X", "1"), 2) & val

def expand_mask(mask, val):
    result = ""
    for i, c in enumerate(format(val, "b").rjust(len(mask), "0")):
        result += c if mask[i] == "0" else mask[i]
    expanded = [['0', '1'] if char == "X" else [char] for char in result]
    masks = list(map("".join, itertools.product(*expanded)))
    return masks

def run_op(op, mask, mem, version):
    action, _, val = op.split(" ")
    if action == "mask":
        return (val, mem)
    else:
        addr_val = int(action.replace("mem[", "").replace("]", ""))
        if version == 1:
            mem[addr_val] = apply_mask(mask, int(val))
        else:
            for addr in expand_mask(mask, addr_val):
                mem[addr] = int(val)
    return (mask, mem)

for answer in [1, 2]:
    mask = ""
    mem = dict()
    for op in ops:
        mask, mem = run_op(op, mask, mem, answer)

    total = sum(mem.values())
    print(f"answer {answer}: {total}")