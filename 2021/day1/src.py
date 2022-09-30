from functools import reduce

with open("input.txt", "r") as f:
    # read all sonar sweeps as the integer values of the lines in the input file
    sweeps = [int(line) for line in f]

# take a tuple of the previous value and increase counts so far
# as well as the current value
# return a tuple of the current value and the new count
def count_increases(prev, curr):
    prev_val, count = prev
    if curr > prev_val:
        count += 1
    return (curr, count)

# reduce the list of sweeps to count the increases
result = reduce(count_increases, sweeps[1:], (sweeps[0], 0))
print(f"Solution 1: {result[1]}")

# create the windows by zipping the sweeps against themselves shifted right once and twice
windows = zip(sweeps, sweeps[1:], sweeps[2:])
# sum up the windows, and convert to a proper list so it can be subscripted below
sums = list(map(sum, windows))
# count increases the same way as above
result = reduce(count_increases, sums[1:], (sums[0], 0))
print(f"Solution 2: {result[1]}")