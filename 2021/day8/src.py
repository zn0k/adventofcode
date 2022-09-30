digits = {"0": "abcefg", "1": "cf","2": "acdeg","3": "acdfg","4": "bcdf","5": "abdfg","6": "abdefg","7": "acf","8": "abcdefg","9": "abcdfg"}
# each line segment is present a certain number of times across all ten digits. count how often that is
concat = "".join(digits.values())
counts = {c: concat.count(c) for c in "abcdefg"}

# generate a lookup table that expresses each digit in terms
# of how often its line segments appear, in ascending sort order}
lookup = {}
for digit, value in digits.items():
    key = "".join(sorted([str(counts[c]) for c in value]))
    lookup[key] = digit

with open("8-100000.in", "r") as f:
    signals = []
    for line in f:
        front, back = line.rstrip().split(" | ")
        signals.append((front.split(" "), back.split(" ")))

def translate(signal):
    front, back = signal
    # generate counts for all the line segments in the front
    # part of the signal, which is the ten digits in some unknown format
    concat = "".join(front)
    counts = {s: str(concat.count(s)) for s in "abcdefg"}
    # map the back part of the signal to the lookup
    result = ""
    for digit in back:
        key = "".join(sorted([counts[c] for c in digit]))
        result += lookup[key]
    return result

translated = list(map(translate, signals))

concat = "".join(translated)
result = sum(map(lambda x: concat.count(x), "1478"))
print(f"Solution 1: {result}")

result = sum(map(int, translated))
print(f"Solution 2: {result}")