#!/usr/bin/env python3

import sys

def readInput():
  cards = []
  with open(sys.argv[1], "r") as f:
    for line in f.readlines():
      fields = line.strip().replace(":", " |").split("| ")
      winners = list(map(int, fields[1].split()))
      haves = list(map(int, fields[2].split()))
      cards.append((winners, haves))
  return cards

# games = [(winners, haves), ...]
games = readInput()

# count the number of matches in the haves for each game
games = [[x in winners for x in haves].count(True) for winners, haves in games]

# each game scores 2^(num_wins-1), also filter out games that didn't win at all
points = map(lambda x: 2 ** x, [x - 1 for x in games if x > 0])

print(f"Solution 1: {sum(points)}")

# initially, there's one copy of each card
copies = [1 for game in games]
# go through each card
for i, wins in enumerate(games):
  # add the copies for the offset
  for j in range(i + 1, i + wins + 1):
    # check out of bounds before adding that many copies
    if j < len(copies): copies[j] += copies[i]

print(f"Solution 2: {sum(copies)}")