#!/usr/bin/env python3

import sys

with open(sys.argv[1], "r") as f:
    chunks = f.read().split("\n\n")

r = [c.split() for c in chunks[0].split("\n")]
r = {x[1][0]: int(x[2]) for x in r}
program = chunks[1].split("Program: ")[1]
program = list(int(x) for x in program.split(","))


def run(program, a, b, c):
    def combo(op):
        if op >= 4:
            return (a, b, c)[op - 4]
        else:
            return op

    ip = 0
    output = []

    while ip < len(program):
        opcode, operand = program[ip], program[ip + 1]
        match opcode:
            case 0:
                a //= 2 ** combo(operand)
            case 1:
                b ^= operand
            case 2:
                b = combo(operand) & 7
            case 3:
                if a:
                    ip = operand - 2
            case 4:
                b ^= c
            case 5:
                output.append(combo(operand) & 7)
            case 6:
                b = a // (2 ** combo(operand))
            case 7:
                c = a // (2 ** combo(operand))
        ip += 2
    return output


part1 = ",".join(map(str, run(program, r["A"], r["B"], r["C"])))
print(f"Solution 1: {part1}")

# bst operand=4, ip=0, a=18427963, b=0, c=0
# bxl operand=1, ip=2, a=18427963, b=3, c=0
# cdv operand=5, ip=4, a=18427963, b=2, c=0
# adv operand=3, ip=6, a=18427963, b=2, c=4606990
# bxc operand=3, ip=8, a=2303495, b=2, c=4606990
# bxl operand=6, ip=10, a=2303495, b=4606988, c=4606990
# out operand=5, ip=12, a=2303495, b=4606986, c=4606990
# jnz operand=0, ip=14, a=2303495, b=4606986, c=4606990
# this is the core loop of the program, which runs until a=0

# given the operands, it performs these steps in order during loop iteration i:
# 1. bst 4 => B = A[i] % 8
# 2. bxl 1 => B = B ^ 1
# 3. cdv 5 => C = A[i] // 2**B
# 4. adv 3 => a[i+1] = A[i] // 8
# 5. bxc 3 =? B = B ^ C
# 6. bxl 6 => B = B ^ 6
# 7. out 5 => output B % 8
# 8. jnz => do it again unless A has been reduced to 0

# function that performs one loop iteration given an A value
# it returns the next A value and the output from the loop iteration
def iterate(A):
    B = A % 8
    B ^= 1
    C = A // (2**B)
    A_next = A // 8
    B ^= C
    B ^= 6
    return A_next, B % 8


# function that finds candidate values that generate the right next
# value of A as well as the right desired output
def find_candidates(A_next, out):
    candidates = []
    base = A_next * 8
    for i in range(8):
        candidate = base + i
        candidate_A_next, candidate_out = iterate(candidate)
        if candidate // 8 == candidate_A_next and candidate_out == out:
            candidates.append(candidate)
    return candidates


# backtrack through the register A values we need to generate
# works its way through the program in reverse
def find_A(program, index, A_next):
    if index < 0:
        return A_next
    target = program[index]
    candidates = find_candidates(A_next, target)
    if not candidates:
        return None
    for c in candidates:
        result = find_A(program, index - 1, c)
        if result:
            return result
    return None


part2 = find_A(program, len(program) - 1, 0)
print(f"Solution 2: {part2}")
