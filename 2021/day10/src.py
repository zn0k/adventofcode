from collections import deque
from typing import NamedTuple
from functools import reduce

class Line(NamedTuple):
    penalty: int
    stack: deque

with open("10-10000-10000.in", "r") as f:
    lines = [l.rstrip() for l in f]

penalties = {")": 3, "]": 57, "}": 1197, ">": 25137}
char_scores = {"(": 1, "[": 2, "{": 3, "<": 4}
openers = "([{<"
closers = ")]}>"

def process_line(line: str) -> Line:
    def get_closing(char: str) -> str:
        if char in openers:
            return closers[openers.index(char)]
        return ""
    stack = deque()
    for char in line:
        if char in openers:
            stack.append(char)
        else:
            opener = stack.pop()
            if not char == get_closing(opener): return Line(penalties[char], stack)
    return Line(0, stack)

def score_stack(lst: Line) -> int:
    def calculate_score(score: int, char: str) -> int:
        score *= 5
        return score + char_scores[char]
    return reduce(calculate_score, reversed(lst.stack), 0)

processed = list(map(process_line, lines))
score = sum(map(lambda line: line.penalty, processed))
print(f"Solution 1: {score}")

corrupt = filter(lambda line: not line.penalty, processed)
scores = sorted(map(score_stack, corrupt))
score = scores[len(scores) // 2]
print(f"Solution 2: {score}")