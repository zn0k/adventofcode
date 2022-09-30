with open("input.txt", "r") as f:
    points = []
    folds = []
    for line in f:
        if "," in line: 
            points.append(tuple(map(int, line.rstrip().split(","))))
        elif "=" in line: 
            words = line.rstrip().split(" ")
            dimension, size = words[2].split("=")
            folds.append((dimension, int(size)))

def print_page(page):
    for line in page:
        print("".join(map(str, line)).replace("1", "#").replace("0", " "))

def add(a, b):
    return [[max(a[y][x], b[y][x]) for x in range(len(a[y]))] for y in range(len(a))]

def fold_vertical(page, cut):
    top = page[0:cut]
    bottom = list(reversed(page[cut + 1:]))
    return add(top, bottom)

def fold_horizontal(page, cut):
    left = [line[0:cut] for line in page]
    right = [list(reversed(line[cut + 1:])) for line in page]
    return add(left, right)

def count_dots(page):
    return sum([sum(line) for line in page])

max_x = 2 * max(map(lambda x: x[1], filter(lambda x: x[0] == "x", folds)))
max_y = 2 * max(map(lambda x: x[1], filter(lambda x: x[0] == "y", folds)))

page = [[0 for x in range(max_x + 1)] for y in range(max_y + 1)]
for x, y in points:
    page[y][x] = 1

dimension, size = folds[0]
folded = fold_vertical(page, size) if dimension == "y" else fold_horizontal(page, size)
print(f"Solution 1: {count_dots(folded)}")

for dimension, size in folds[1:]:
    folded = fold_vertical(folded, size) if dimension == "y" else fold_horizontal(folded, size)
print("Solution 2:")
print_page(folded)