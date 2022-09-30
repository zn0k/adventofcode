import numpy as np

# read in the initial board
board = np.genfromtxt("11-1000-2.in", dtype="i4", delimiter=1)
height, width = board.shape
ones = np.ones((height, width), dtype="i4")
zeroes = np.zeros((height, width), dtype="i4")

def neighbors(x, y):
    offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    return [(x + v, y + h) for h, v in offsets if 0 <= x + v < width and 0 <= y + h < height]

total_flashes = 0
all_flash = 0

step = 0
while True:
    step += 1
    # increase energy level of each octopus
    board += ones
    # create a lookup table for octopuses that have already flashed
    already_flashed = np.copy(zeroes)
    # loop while there are increases to be made
    keep_looping = True
    while keep_looping:
        # assume we're done after this round
        keep_looping = False
        # go through each octopus and check if its energy level is larger than 9
        for x in range(0, height):
            for y in range(0, width):
                if board[y, x] > 9 and not already_flashed[y, x]:
                    # it is, and hasn't previously flashed
                    # increase its neighbors energy levels
                    for n_x, n_y in neighbors(x, y):
                        board[n_y, n_x] += 1
                    # also mark the octopus itself as having flashed
                    already_flashed[y, x] = 1
                    # mark that something happened this round
                    keep_looping = True
                    # increase flash count
                    if step <= 100: total_flashes += 1

    # reset all energy values of octopuses that flashed
    for y in range(0, height):
        for x in range(0, width):
            if already_flashed[y, x]:
                board[y, x] = 0

    # check if all octopuses are at 0 to record they synchronized
    if all_flash == 0 and not np.any(board): 
        all_flash = step
        break

print(f"Solution 1: {total_flashes}")    
print(f"Soltuion 2: {all_flash}")