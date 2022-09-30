from collections import deque
from itertools import islice

input_file = "input.txt"

def initialize(file):
    with open(file, "r") as f:
        paragraphs = f.read().split("\n\n")
        deckA = [int(x) for x in paragraphs[0].split("\n")[1::]]
        deckB = [int(x) for x in paragraphs[1].split("\n")[1::]]
    return (deckA, deckB)

def play_round(a, b):
    if a[0] > b[0]:
        return (a[1::] + [a[0], b[0]], b[1::])
    else:
        return (a[1::], b[1::] + [b[0], a[0]])

def score(deck):
    with_position = zip(reversed(deck), range(1, len(deck) + 1))
    return sum(map(lambda x: x[0] * x[1], with_position))

deckA, deckB = initialize(input_file)

while len(deckA) and len(deckB):
    deckA, deckB = play_round(deckA, deckB)

winning_score = score(deckA) if len(deckA) else score(deckB)
print(f"Answer 1: {winning_score}")

iterations = 0

def play_recursive_round(deck_a, deck_b, history):
    #print(f"play_recursive_round called with {deck_a}, {deck_b}, {history}")
    lookup = str(deck_a) + "|" + str(deck_b)
    if lookup in history: return (deck_a, [], "A", history)
    history[lookup] = 1

    winner = ""
    a, b = deck_a.popleft(), deck_b.popleft()
    #print(f"now {deck_a} and {deck_b} with first elements {a} and {b}")
    if len(deck_a) >= a and len(deck_b) >= b:
        sub_a = deque(list(islice(deck_a, 0, a)))
        sub_b = deque(list(islice(deck_b, 0, b)))
        sub_history = {}
        #print(f"playing subgame with {sub_a} and {sub_b}")
        while sub_a and sub_b:
            sub_a, sub_b, winner, sub_history = play_recursive_round(sub_a, sub_b, sub_history)
        if winner == "A":
            #print("A won subgame")
            deck_a.extend([a, b])
            return (deck_a, deck_b, "A", history)
        else:
            #print("B won subgame")
            deck_b.extend([b, a])
            return (deck_a, deck_b, "B", history)
    if (winner and winner == "A") or a > b:
        deck_a.extend([a, b])
        #print(f"A won, returning {deck_a} and {deck_b}")
        return (deck_a, deck_b, "A", history)
    else:
        deck_b.extend([b, a])
        #print(f"B won, returning {deck_a} and {deck_b}")
        return (deck_a, deck_b, "B", history)

history = {}
deckA, deckB = map(deque, initialize(input_file))
while deckA and deckB:
    deckA, deckB, winner, history = play_recursive_round(deckA, deckB, history)
winning_score = score(deckA) if len(deckA) else score(deckB)
print(f"Answer 2: {winning_score}")