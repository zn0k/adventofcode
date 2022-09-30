def get_start():
    with open("input.txt", "r") as f:
        return [int(x) for line in f.readlines() for x in line.split(",")]

def dist(nums, num):
    if nums.count(num) >= 2:
        last = len(nums) - nums[::-1].index(num) - 1
        rest = nums[:last]
        return last - (len(rest) - rest[::-1].index(num) - 1)
    else:
        return 0

nums = get_start()
iterations = 2020 - len(nums)
for i in range(0, iterations):
    last = nums[-1]
    nums.append(dist(nums, last))

print(f"answer 1: {nums[-1]}")

def speak(num, turn):
    if num in past:
        previous = past[num]
        past[num] = turn - 1
        return turn - 1 - previous
    else:
        past[num] = turn - 1
        return 0

past = {}
nums = get_start()
for i, num in enumerate(nums[:-1]):
    past[num] = i + 1

last = nums[-1]
for turn in range(len(nums) + 1, 30000000 + 1):
    last = speak(last, turn)
print(f"answer 2: {last}")