from collections import deque

with open("input.txt", "r") as f:
    fish = [int(x) for x in f.readlines()[0].split(",")]

# don't keep track of fish, keep track of how many fish 
# with each possible timer (0-8) there are
# the index of the list corresponds to the timer value
fish = deque([fish.count(x) for x in range(0, 9)])

# solve total population for given number of days
def solve(days):
    result = fish.copy()
    for x in range(0, days):
        # shift left to rotate timers and reproduce
        result.rotate(-1)
        # original fish that rotated should be in timer 6, add them there
        result[6] += result[-1]
    # and sum it up
    return sum(result)

def display(result):
    stringified = str(result)
    if len(stringified) > 30:
        stringified = stringified[0:10] + "..." + stringified[len(stringified) - 10:]
    return stringified

print(f"Solution 1: {solve(80)}")
print(f"Solution 2: {solve(256)}")
#print(f"Solution big 1: {display(solve(999999))}")
