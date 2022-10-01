from collections import OrderedDict
from math import sqrt

def chunks(lst, n):
    for i in range(0, len(lst), n): yield lst[i:i+n]

def assemble_board(lines):
    return [(int(x), False) for x in " ".join(lines).split() if x]

with open("input.txt", "r") as f:
    lines = [l.rstrip() for l in f]
    draws = map(int, lines[0].split(","))
    boards = [assemble_board(board) for board in chunks(lines[2:], lines[2:].index("") + 1)]

def mark_draw(draw, board):
    def match(field):
        value, matched = field
        return (value, True) if not matched and value == draw else field
    return [match(f) for f in board]

def is_winner(board):
    size = int(sqrt(len(board)))
    marked = [f[1] for f in board]
    verticals = zip(*[marked[x:] for x in range(0, size * size, size)])
    horizontals = [marked[x:x+size] for x in range(0, size * size, size)]
    return any(map(all, verticals)) or any(map(all, horizontals))

def score_boards(draw, boards, scores, win_state):
    def unmarked_values(board):
        return [f[0] for f in board if not f[1]]
    def score(board, previous_score):
        return max([draw * sum(unmarked_values(board)), previous_score])
    return [score(boards[i], scores[i]) if winner else 0 for i, winner in enumerate(win_state)]

winners = OrderedDict()
scores = [0 for _ in boards]
for draw in draws:
    boards = [mark_draw(draw, b) for b in boards]
    win_state = [is_winner(b) for b in boards]
    winners.update({x: None for x in [i for i, winner in enumerate(win_state) if winner]})
    scores = score_boards(draw, boards, scores, win_state)
    if all(scores): break

in_order = list(winners.keys())
print(f"Solution 1: {scores[in_order[0]]}")
print(f"Solution 2: {scores[in_order[-1]]}")