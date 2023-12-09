#!/usr/bin/env python3

import sys
from collections import Counter
from functools import cmp_to_key

with open(sys.argv[1], "r") as f:
  hands = [line.strip().split() for line in f.readlines()]

# generic function to compare two hands given a function that 
# returns the hand's type as per CMP spec, and a string that 
# shows the order of possible cards in the deck
def cmpHands(a, b, typefunc, cardorder):
  typeA, typeB = typefunc(Counter(a[0])), typefunc(Counter(b[0]))
  if typeA > typeB: return 1
  if typeA < typeB: return -1
  # they're the type hands, so compare the cards left to right
  for idx in range(len(a[0])):
    posA, posB = cardorder.index(a[0][idx]), cardorder.index(b[0][idx])
    if posA > posB: return 1
    if posB > posA: return -1
  # fall through to hands being the exact same
  return 0

def sortPart1(a, b):
  def handType(hand):
    # create a score for the hand type based on how many of a kinds there are
    return sum(map(lambda x: 10 ** x[1], hand.items()))
  return cmpHands(a, b, handType, "23456789TJQKA")

# sort the hands
part1 = sorted(hands, key=cmp_to_key(sortPart1))
# score each hand
part1 = map(lambda x: (x[0] + 1) * int(x[1][1]), enumerate(part1))

print(f"Solution 1: {sum(part1)}")

def sortPart2(a, b):
  def handType(hand):
    if "J" in hand:
      # there's a joker, record how many and remove them
      jokers = hand["J"]
      del hand["J"]
      # check if there are non-jokers left
      if len(hand.keys()):
        # find one of the most common remaining cards, add that many jokers
        hand.update(hand.most_common(1)[0][0] * jokers)
      else:
        # must have been all jokers, add 5 of them back in
        hand.update("JJJJJ")
    # create score like before
    return sum(map(lambda x: 10 ** x[1], hand.items()))
  return cmpHands(a, b, handType, "J23456789TQKA")

part2 = sorted(hands, key=cmp_to_key(sortPart2))
part2 = map(lambda x: (x[0] + 1) * int(x[1][1]), enumerate(part2))

print(f"Solution 2: {sum(part2)}")
