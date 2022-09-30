with open("input.txt", "r") as f:
    lines = [l.rstrip() for l in f]
    lookup = [1 if c == "#" else 0 for c in lines[0]]
    image = []
    for line in lines[2:]:
        line = [1 if c == "#" else 0 for c in line]
        image.append(line)

offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

def enhance(image, steps):
    # this took too long to figure out. the sample data has a "." as the first
    # character in the first line. if it's a #, what infinity pixels should be
    # depends on the step you're on, and isn't always just turned off
    if lookup[0] == 0: infinity = lambda _: 0
    else: infinity = lambda step: 1 if step % 2 else 0
    for step in range(steps):
        new_image = []
        for y in range(-1, len(image) + 1):
            line = []
            for x in range(-1, len(image[0])+ 1):
                binary = ""
                for dx, dy in offsets:
                    if dx + x < 0 or dx + x >= len(image[0]): value = infinity(step)
                    elif dy + y < 0 or dy + y >= len(image): value = infinity(step)
                    else: value = image[dy + y][dx + x]
                    binary += "1" if value else "0"
                binary = int(binary, 2)
                line.append(lookup[binary])
            new_image.append(line)
        image = new_image
    return image

count = sum(map(sum, enhance(image.copy(), 2)))
print(f"Solution 1: {count}")

count = sum(map(sum, enhance(image.copy(), 50)))
print(f"Solution 2: {count}")