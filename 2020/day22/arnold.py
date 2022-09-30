def fill_deck(file):
    line = f.readline().strip()
    deck = []
    while line:
        if "Player" in line:
            line = f.readline().strip()
        else:
            deck.append(int(line.strip()))
            line = f.readline().strip()
    return deck
def step(deck1, deck2):
    if deck1[0] > deck2[0]:
        deck1 = deck1[1:] + [ deck1[0], deck2[0] ]
        if len(deck2) > 1:
            deck2 = deck2[1:]
        else:
            deck2 = []
    else:
        deck2 = deck2[1:] + [ deck2[0], deck1[0] ]
        if len(deck1) > 1:
            deck1 = deck1[1:]
        else:
            deck1 = []
    return deck1, deck2
def calc_score(deck):
    deck = deck[::-1]
    score = sum([ mult*card for mult, card in zip(range(1, len(deck)+1), deck) ] )
    return score
def play_game1(deck1, deck2):
    while len(deck1) > 0 and len(deck2) > 0:
        deck1, deck2 = step(deck1, deck2)
    return deck1, deck2
with open('input.txt') as f:
    deck1 = fill_deck(f)
    line = f.readline()
    deck2 = fill_deck(f)
deck1, deck2 = play_game1(deck1, deck2)
if len(deck1) > 0:
    print(calc_score(deck1))
else:
    print(calc_score(deck2))
# Problem 2
# =========
import time
def play_game2(deck1, deck2):
    history1 = []
    history2 = []
    num_steps = 0
    while len(deck1) > 0 and len(deck2) > 0:
        if deck1 in history1 or deck2 in history2:
            return deck1, [], num_steps
        else:
            history1.append(deck1)
            history2.append(deck2)
        if deck1[0] < len(deck1) and deck2[0] < len(deck2):
            sub_deck1, sub_deck2, sub_steps = play_game2(deck1[1:deck1[0]+1], deck2[1:deck2[0]+1])
            num_steps += sub_steps
            if len(sub_deck1) > 0:
                deck1 = deck1[1:] + [ deck1[0], deck2[0] ]
                if len(deck2) > 1:
                    deck2 = deck2[1:]
                else:
                    deck2 = []
            else:
                deck2 = deck2[1:] + [ deck2[0], deck1[0] ]
                if len(deck1) > 1:
                    deck1 = deck1[1:]
                else:
                    deck1 = []
        else:
            deck1, deck2 = step(deck1, deck2)
            num_steps += 1
    return deck1, deck2, num_steps
startTime = time.time()
with open('input.txt') as f:
    deck1 = fill_deck(f)
    line = f.readline()
    deck2 = fill_deck(f)
deck1, deck2, num_steps = play_game2(deck1, deck2)
if len(deck1) > 0:
    print(num_steps, calc_score(deck1))
else:
    print(num_steps, calc_score(deck2))