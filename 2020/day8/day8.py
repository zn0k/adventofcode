def parse_op(line):
    op, offset = line.split(" ")
    return (op, "-" if offset.startswith("-") else "+", int(offset[1::]))

with open("input.txt", "r") as f:
    ops = f.read().split("\n")
    ops = list(map(parse_op, ops))

def acc(i, acc, direction, offset):
    # set the new accumulator value, go to next op
    return (i + 1, acc - offset if direction == "-" else acc + offset)

def nop(i, acc, direction, offset):
    # do nothing, go to next op
    return (i + 1, acc)

def jmp (i, acc, direction, offset):
    # leave accumulator alone, jump to indicated op
    return (i - offset if direction == "-" else i + offset, acc)

dispatch = {"acc": acc, "nop": nop, "jmp": jmp}

def run_program_protect_loop(ops, i, acc, executed):
    if i == len(ops):
        # jumped to op after last one, program completed successfully
        return (True, acc)
    if i in executed or i > len(ops):
        # infinite loop, or jumped to an op that doesn't exist. error out
        return (False, acc)
    # mark current op as seen
    executed.append(i)
    (op, direction, offset) = ops[i]
    # get the new op index and new accumulator based on the current op
    (i, acc) = dispatch[op](i, acc, direction, offset)
    # run next op
    return run_program_protect_loop(ops, i, acc, executed)            

success, acc = run_program_protect_loop(ops, 0, 0, [])
if success == False:
    print(f"Accumulator is {acc}, but code is faulty")

# go through all ops and try to patch them one by one, running the set each time
for i in range(0, len(ops)):
    (op, direction, offset) = ops[i]
    if op == "acc":
        # can't patch acc ops, so skip it
        continue
    else:
        # current op is a jmp or nop
        # first, make a copy of the entire op set
        patched_ops = ops.copy()
        # patch the current op by swapping jmp and nop
        patched_ops[i] = ("jmp" if op == "nop" else "nop", direction, offset)
    # try to run the set
    success, acc = run_program_protect_loop(patched_ops, 0, 0, [])
    if success:
        print(f"Patched instruction at index {i}, accumulator is {acc}")
        break