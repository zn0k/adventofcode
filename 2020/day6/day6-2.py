with open("input.txt", "r") as f:
    groups = f.read().split("\n\n")
    groups = [[set(x) for x in group.split("\n")] for group in groups]

union_count = sum([len(set.union(*x)) for x in groups])
print(f"Union count is {union_count}")
intersection_count = sum([len(set.intersection(*x)) for x in groups])
print(f"Intersection count is {intersection_count}")