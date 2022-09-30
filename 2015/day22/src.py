from dataclasses import dataclass

with open("input.txt", "r") as f:
    instructions = []
    for line in f:
        instruction = [line[0:3]]
        rest = line[4:-1]
        args = rest.split(", ")
        instructions.append(tuple(instruction + args))

@dataclass
class Computer:
    a: int
    b: int
    pointer: int

def hlf(c, r):
    if r == "a": c.a /= 2
    else: c.b /= 2
    c.pointer += 1
    return c

def tpl(c, r):
    if r == "a": c.a *= 3
    else: c.b *= 3
    c.pointer += 1
    return c

def inc(c, r):
    if r == "a": c.a += 1
    else: c.b += 1
    c.pointer += 1
    return c

def jmp(c, offset):
    c.pointer += int(offset)
    return c

def jie(c, r, offset):
    val = c.a if r == "a" else c.b
    c.pointer += int(offset) if val % 2 == 0 else 1
    return c

def jio(c, r, offset):
    val = c.a if r == "a" else c.b
    c.pointer += int(offset) if val == 1 else 1
    return c

dispatch = {"hlf": hlf, "tpl": tpl, "inc": inc, "jmp": jmp, "jie": jie, "jio": jio}

computer = Computer(0, 0, 0)
while(computer.pointer < len(instructions)):
    instruction, *args = instructions[computer.pointer]
    computer = dispatch[instruction](computer, *args)

print(f"Solution 1: {computer.b}")

computer = Computer(1, 0, 0)
while(computer.pointer < len(instructions)):
    instruction, *args = instructions[computer.pointer]
    computer = dispatch[instruction](computer, *args)

print(f"Solution 2: {computer.b}")

