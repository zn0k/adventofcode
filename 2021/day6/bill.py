#!/usr/bin/python3

# Read input file into a startingfish list
with open("input_test.txt", "r") as inputfile:
   startingfish = [int(f) for f in inputfile.readline().rstrip().split(',')]

# Convert startingfish list to list with number of each timer value
# where index is the timer value
# timers = ['num0', 'num1', ... 'num6', 'num7', 'num8']
timers = [0] * 9
for t in range(len(timers)):
   timers[t] = startingfish.count(t)

for day in range(9999999):
   # Decrease timers by moving left one slot
   spawns = timers.pop(0)
   # Add new spawns in eighth slot
   timers.append(spawns)
   # Reset spawned fish to 6
   timers[6] += spawns

print(sum(timers))
