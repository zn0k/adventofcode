#!/usr/bin/env python3

import sys
from functools import reduce

def readInput():
  games = {}
  with open(sys.argv[1], "r") as f:
    for line in f.readlines():
      # parse each line. first, split by colon to get the game ID
      game_id, rest = line.strip().split(": ")
      _, game_id = game_id.split(" ")
      game_id = int(game_id)
      # prepare a list of rounds for the game
      games[game_id] = []
      # each round in a game splits by semi-colon
      rounds = rest.split("; ")  
      for round in rounds:
        # cube colors and their numbers are split by comma
        cubes = round.split(", ")
        round = {"red": 0, "green": 0, "blue": 0}
        for cube in cubes:
          num, color = cube.split(" ")
          round[color] = int(num)
        games[game_id].append(round)
  return games

games = readInput()

valid_game = lambda rounds: all(map(lambda x: x["red"] <= 12 and x["green"] <= 13 and x["blue"] <= 14, rounds))
valid = {k: v for k, v in games.items() if valid_game(v)}

print(f"Solution 1: {sum(valid.keys())}")

def game_power(rounds):
  reds = [r["red"] for r in rounds]
  greens = [r["green"] for r in rounds]
  blues = [r["blue"] for r in rounds]
  return max(reds) * max(greens) * max(blues)

powers = [game_power(v) for k, v in games.items()]
print(f"Solution 2: {sum(powers)}")