with open("input.txt", "r") as f:
    sizes = list(map(int, f.readlines()))

target = 150

def matching_subsets(nums, target, partial=[], partial_sum=0):
    if partial_sum == target:
        yield partial
    if partial_sum >= target:
        return
    for i, n in enumerate(nums):
        remaining = nums[i + 1:]
        yield from matching_subsets(remaining, target, partial + [n], partial_sum + n)

solutions = list(matching_subsets(sizes, target))
print(f"Solution 1: {len(solutions)}")

smallest_size = min(map(lambda x: len(x), solutions))
smallest_solutions = list(filter(lambda x: len(x) == smallest_size, solutions))
print(f"Solution 2: {len(smallest_solutions)}")