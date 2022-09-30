with open("input.txt", "r") as f:
    _, _, _, x, _, y = f.readlines()[0].rstrip().replace("=", "= ").split()
    t_min_x, t_max_x = map(int, x.rstrip(",").split(".."))
    t_min_y, t_max_y = map(int, y.split(".."))

dx_max = max([abs(t_min_x), abs(t_max_x)]) + 1
dy_max = max([abs(t_min_y), abs(t_max_y)]) + 1

cutoff_y = (t_min_y if t_min_y < t_max_y else t_max_y)

max_y = 0
paths = 0
for starting_dx in range(0, dx_max):
    for starting_dy in range(-1 * dy_max, dy_max):
        x, y = (0, 0)
        dx = starting_dx
        dy = starting_dy
        local_max_y = 0
        while True:
            x += dx
            y += dy
            if y > local_max_y:
                local_max_y =y
            if t_min_x <= x <= t_max_x and t_min_y <= y <= t_max_y:
                if local_max_y > max_y:
                    max_y = local_max_y
                paths += 1
                break
            if y < cutoff_y:
                break
            if dx > 0:
                dx -= 1
            elif dx < 0:
                dx += 1
            dy -= 1

print(f"Solution 1: {max_y}")
print(f"Solution 2: {paths}")