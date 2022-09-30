from functools import reduce 

# create a list of moves 
# it consists of tuples like ("forward", 5)
moves = []
with open("input.txt", "r") as f:
    for line in f:
        direction, magnitude = line.split(" ")
        moves.append((direction, int(magnitude)))

# get all moves into a certain direction from the list of moves
def filter_direction(direction):
    return filter(lambda x: x[0] == direction, moves)

# sum all the magnitude elements from a list of tuples
def sum_moves(direction):
    return sum(map(lambda x: x[1], filter_direction(direction)))

# calculate the final horizontal and vertical position
x = sum_moves("forward")
y = sum_moves("down") - sum_moves("up")

print(f"Solution 1: {x * y}")

def forward(magnitude, position):
    x, y, aim = position
    return (x + magnitude, y + aim * magnitude, aim)

def up(magnitude, position):
    x, y, aim = position
    return (x, y, aim - magnitude)

def down(magnitude, position):
    x, y, aim = position
    return (x, y, aim + magnitude)

dispatch = {"forward": forward, "up": up, "down": down}

def make_move(position, move):
    direction, magnitude = move
    return dispatch[direction](magnitude, position)

final = reduce(make_move, moves, (0, 0, 0))
print(f"Solution 2: {final[0] * final[1]}")