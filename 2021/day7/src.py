import numpy as np

with open("input.txt", "r") as f:
    positions = [int(x) for x in f.readlines()[0].split(",")]

# best position is the median of the list
median = int(np.median(positions))
# calculate offsets and sum them
fuel = sum([abs(median - x) for x in positions])
print(f"Solution 1: {fuel}")

# new best position is near the mean of the list, either its floor or its ceiling
# calculate both, choose the minimum
mean = np.mean(positions)
floor = int(np.floor(mean))
ceiling = int(np.floor(mean))

# pre-calculate all distances in a data structure
# where the index is the distance, and the value is the corresponding fuel use
# do so by just adding the index to the previous sum
distances = [0]
for x in range(1, max(positions) + 1):
    distances.append(x + distances[-1])

# look up fuel use for each distance by floor and ceiling
fuel_floor = sum([distances[abs(floor - x)] for x in positions])
fuel_ceiling = sum([distances[abs(ceiling - x)] for x in positions])
# pick the smaller one
fuel = min(fuel_floor, fuel_ceiling)
print(f"Solution 2: {fuel}")