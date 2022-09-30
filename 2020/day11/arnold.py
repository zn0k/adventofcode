# Problem one
# -----------
import numpy as np
import copy
def check_adjacent(seats, test_kernel):
    # Trim kernel
    test_kernel = test_kernel[:seats.shape[0], :seats.shape[1]]
    return np.sum(seats==test_kernel)
kernel = np.array([['#', '#', '#'],
                   ['#', '#', '#'],
                   ['#', '#', '#']])
with open('input.txt') as f:
    seat_array = np.array([ list(line.strip()) for line in f.readlines() ])
m,n = seat_array.shape
change = True
while change == True:
    change = False
    next_step = copy.copy(seat_array)
    for i in range(m):
        for j in range(n):
            if seat_array[i,j] != '.':
                n_adj = check_adjacent(seat_array[max(0,i-1):min(i+2,m), max(0,j-1):min(j+2,n)], kernel)
                if seat_array[i,j] == '#' and n_adj >= 5:
                    next_step[i,j] = 'L'
                    change = True
                elif seat_array[i,j] == 'L' and n_adj == 0:
                    next_step[i,j] = '#'
                    change = True
    seat_array = next_step
n_occupied = np.sum(seat_array=='#')
print(f"{n_occupied}")
# Problem two
# -----------
import numpy as np
import copy
def check_first(array, position):
    num_visible = 0
    directions = [[-1, 0], # N
                  [-1, 1], # NE
                  [0,  1],  # E
                  [1,  1],  # SE
                  [1,  0],  # S
                  [1, -1],  # SW
                  [0, -1],  # W
                  [-1,-1]  # NW
                 ]
    # Test directions
    # -------------------
    m,n = array.shape
    for direction in directions:
        flag = True
        i, j = position
        i += direction[0]
        j += direction[1]
        if i < 0 or i >= m or j < 0 or j >= n:
            flag = False
        while flag:
            if array[i,j] == '#':
                num_visible += 1
                break
            elif array[i,j] == 'L':
                break
            i += direction[0]
            j += direction[1]
            if i < 0 or i == m or j < 0 or j == n:
                flag = False
    return num_visible
with open('input.txt') as f:
    seat_array = np.array([ list(line.strip()) for line in f.readlines() ])
m,n = seat_array.shape
change = True
while change == True:
    change = False
    next_step = copy.copy(seat_array)
    for i in range(m):
        for j in range(n):
            if seat_array[i,j] != '.':
                n_adj = check_first(seat_array, [i,j])
                if seat_array[i,j] == '#' and n_adj >= 5:
                    next_step[i,j] = 'L'
                    change = True
                elif seat_array[i,j] == 'L' and n_adj == 0:
                    next_step[i,j] = '#'
                    change = True
    seat_array = next_step
n_occupied = np.sum(seat_array=='#')
print(n_occupied)

