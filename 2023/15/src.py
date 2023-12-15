#!/usr/bin/env python3

import sys

with open(sys.argv[1], "r") as f:
  steps = f.readlines()[0].strip().split(",")

def hash(input):
  result = 0
  for letter in input:
    result += ord(letter)
    result *= 17
    result %= 256
  return result

values = list(map(hash, steps))
print(f"Solution 1: {sum(values)}")

def process_step(step):
  if "-" in step:
    box = step.rstrip("-")
    return ["-", hash(box), box]
  if "=" in step:
    parts = step.split("=")
    return ["=", hash(parts[0]), parts[0], parts[1]]
  return step

boxes = [[] for _ in range(256)]
steps = list(map(process_step, steps))

for step in steps:
  match step[0]:
    case "-":
      box, label = step[1:]
      boxes[box] = [(l, f) for l, f in boxes[box] if l != label]
    case "=":
      box, label, f = step[1:]
      labels = {l[0]: i for i, l in enumerate(boxes[box])}
      if label in labels:
        boxes[box][labels[label]] = (label, f)
      else:
        boxes[box].append((label, f))

total = 0
for box_index, box in enumerate(boxes):
  for slot_index, lens in enumerate(box):
    _, focal_length = lens
    total += ((box_index + 1) * (slot_index + 1) * int(focal_length))

print(f"Solution 2: {total}")