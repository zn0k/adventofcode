#!/usr/bin/env python3

import sys
from collections import deque
from operator import mul
from functools import reduce

def parse_rule(rule):
  if ":" in rule:
    comp, target = rule.split(":")
    if "<" in comp:
      var, op = comp.split("<")
      return ("LT", var, int(op), target)
    if ">" in comp:
      var, op = comp.split(">")
      return ("GT", var, int(op), target)
  return ("GOTO", rule)

with open(sys.argv[1], "r") as f:
  chunks = f.read().split("\n\n")
  rules = []
  rule_names = {}
  for rule in chunks[0].split("\n"):
    rule = rule.strip()
    name, rest = rule.split("{")
    rest = rest.replace("}", "").split(",")
    rule_names[name] = len(rules)
    rules.append(list(map(parse_rule, rest)))
  items = [l.strip().replace("{", "").replace("}", "").split(",") for l in chunks[1].split("\n")]
  items = [list(map(lambda x: int(x.split("=")[1]), attrs)) for attrs in items]

var_map = {"x": 0, "m": 1, "a": 2, "s": 3}

accepted = []
for item in items:
  idx = rule_names["in"]
  while True:
    finished = False
    for instruction in rules[idx]:
      match instruction[0]:
        case "GOTO":
          target = instruction[1]
          match target:
            case "A":
              accepted.append(item)
              finished = True
              break
            case "R":
              finished = True
              break
            case _:
              idx = rule_names[target]
        case "LT":
          _, var, op, target = instruction
          if item[var_map[var]] < op:
            match target:
              case "A":
                accepted.append(item)
                finished = True
                break
              case "R":
                finished = True
                break
              case _:
                idx = rule_names[target]
                break                
        case "GT":
          _, var, op, target = instruction
          if item[var_map[var]] > op:
            match target:
              case "A":
                accepted.append(item)
                finished = True
                break
              case "R":
                finished = True
                break
              case _:
                idx = rule_names[target]
                break                
    if finished: break

val = sum(map(sum, accepted))
print(f"Solution 1: {val}")

# part 2 is a k-d tree
# break each instruction into separate rules with one condition each
# now it's a tree with "in" at the root. each LT or GT child splits into 
# two branches with reduced space. notate their boundaries, and add up the A leafs