from functools import reduce

with open("input.txt", "r") as f:
    digits = f.readlines()[0].rstrip()

width = 25
height = 6
ppl = width * height
layers = int(len(digits) / (width * height))

layers = [digits[ppl * l:ppl * l + ppl] for l in range(0, layers)]
fewest_zeroes = reduce(lambda x, y: x if x.count("0") < y.count("0") else y, layers)
answer = fewest_zeroes.count("1") * fewest_zeroes.count("2")
print(f"Answer 1: {answer}")

layers = [[c for c in layer] for layer in layers]
pixels = map(lambda x: reduce(lambda y, z: y if y in "01" else z, x), zip(*layers))
pixels = list(map(lambda x: " " if x == "0" else "X", pixels))
image = ""
for row in range(0, height):
    image += "".join(pixels[row * width:row * width + width]) + "\n"
print(image)