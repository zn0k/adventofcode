with open("input.txt", "r") as f:
    _, _, _, x, _, y = f.readlines()[0].rstrip().replace("=", "= ").split()
    x_bounds = list(map(int, x.rstrip(",").split("..")))
    y_bounds = list(map(int, y.split("..")))

dx_max = max(map(abs, x_bounds)) + 1
dy_max = max(map(abs, y_bounds)) + 1

cutoff_y = min(y_bounds)

def velocities(dx_max, dy_max):
    for dx in range(0, dx_max): 
        for dy in range(-1 * dy_max, dy_max): 
            yield (dx, dy)

def check_path(deltas):
    dx, dy = deltas
    x, y, max_y = (0, 0, 0)
    while True:
        x, y = (x + dx, y + dy)
        if y > max_y: max_y = y
        if x_bounds[0] <= x <= x_bounds[1] and y_bounds[0] <= y <= y_bounds[1]: return max_y
        if y < cutoff_y: return None
        dx, dy = (dx - 1 if dx > 0 else (dx + 1 if dx < 0 else dx), dy - 1)

paths = list(filter(lambda x: x is not None, map(check_path, velocities(dx_max, dy_max))))

print(f"Solution 1: {max(paths)}")
print(f"Solution 2: {len(paths)}")