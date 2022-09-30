def get_initial_grid():
    with open("input.txt", "r") as f:
        grid = []
        lines = [x.rstrip() for x in f.readlines()]
        for line in lines:
            grid.append([x for x in line])
    return grid

grid = get_initial_grid()

moves = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
boundary = len(grid)

def print_grid(grid):
    print("\n".join(["".join(x) for x in grid]))
    print("\n")

def filter_neighbors(n):
    x, y = n
    if x < 0 or x >= boundary:
        return False
    if y < 0 or y >= boundary:
        return False
    return True

def count_lit_neighbors(x, y):
    neighbors = [(x + m[0], y + m[1]) for m in moves]
    neighbors = list(filter(filter_neighbors, neighbors))
    neighbor_values = list(map(lambda x: grid[x[0]][x[1]], neighbors))
    return neighbor_values.count("#")

def compute_step():
    new_grid = []
    for x in range(0, boundary):
        new_row = []
        for y in range(0, boundary):
            lit_neighbors = count_lit_neighbors(x, y)
            if grid[x][y] == "#":
                val = "#" if lit_neighbors in [2,3] else "."
            else:
                val = "#" if lit_neighbors == 3 else "."
            new_row.append(val)
        new_grid.append(new_row)
    return new_grid

for i in range(0, 100):
    grid = compute_step()

lit = sum(map(lambda x: x.count("#"), grid))
print(f"Solution 1: {lit}")

def flip_corners():
    for cell in [(0, 0), (0, boundary - 1), (boundary - 1, 0), (boundary - 1, boundary - 1)]:
        x, y = cell
        grid[x][y] = "#"

grid = get_initial_grid()
flip_corners()
for i in range(0, 100):
    grid = compute_step()
    flip_corners()

lit = sum(map(lambda x: x.count("#"), grid))
print(f"Solution 2: {lit}")