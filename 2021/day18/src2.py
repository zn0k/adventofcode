from math import floor, ceil
from functools import reduce
from itertools import combinations

def parse(number):
    return [int(c) if c in "0123456789" else c for c in number.rstrip()]

with open("input.txt", "r") as f:
    numbers = [parse(l) for l in f]

def reduce_number(number):
    number = number.copy()
    def first_num_index(lst):
        for index, token in enumerate(lst): 
            if isinstance(token, int): return index
    def last_num_index(lst):
        r = first_num_index(reversed(lst))
        return len(lst) - r - 1 if r else None
    reducible = True
    while reducible:
        reducible = exploded = False
        depth = 0
        for index, token in enumerate(number):
            if token == "[": depth += 1
            elif token == "]": depth -= 1
            elif token == ",": continue
            elif depth == 5:
                left_index = last_num_index(number[0:index])
                if left_index: number[left_index] += token
                right_index = first_num_index(number[index + 3:])
                if right_index: 
                    right_index += index + 3
                    right = number[index + 2]
                    number[right_index] += right
                number = number[0:index - 1] + [0] + number[index + 4:]
                reducible = exploded = True
                break
        if exploded: continue
        for index, token in enumerate(number):
            if isinstance(token, int):
                if token >= 10:
                    number = number[0:index] + ["[", floor(token / 2), ",", ceil(token / 2), "]"] + number[index + 1:]
                    reducible = True
                    break
    return number

def add(left, right):
    return reduce_number(["["] + left + [","] + right + ["]"])

def magnitude(number):
    return eval("".join(map(str, number.copy())).replace("[", "(").replace("]", ")").replace(",", "*3+2*"))

reduced = reduce(add, numbers)
print(f"Solution 1: {magnitude(reduced)}")

pairs = list(combinations(numbers, 2)) + list(map(lambda x: x[::-1], combinations(numbers, 2)))
sums = map(magnitude, map(lambda x: add(x[0], x[1]), pairs))
print(f"Solution 2: {max(sums)}")
