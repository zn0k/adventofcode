import itertools
import operator
import re
import collections
import functools

with open("input.txt", "r") as f:
    chain = list(map(int, f.read().split("\n")))

chain = sorted(chain + [0] + [max(chain) + 3])

diffs = list(map(lambda x: x[1] - x[0], zip(chain, chain[1::])))
product = diffs.count(3) * diffs.count(1)
print(f"{product}")

def calc_combos(x):
    remainder = 0 if len(x) <= 3 else calc_combos(x[3::])
    return (2 ** (len(x) - 1)) - remainder

seqs = collections.Counter(re.findall("11+", "".join(map(str, diffs))))
combinations = functools.reduce(
    operator.mul, 
    map(lambda x: calc_combos(x[0]) ** x[1], seqs.items()), 
    1)
print(f"{combinations}")