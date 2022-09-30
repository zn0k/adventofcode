from functools import reduce

def factors(n):    
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

threshold = 33100000

num = int(threshold / 43)
while True:
    fs = factors(num)
    presents = sum(map(lambda x: x * 10, fs))
    if presents > threshold:
        break
    num += 1

print(f"Solution 1: {num}")

presents = {x: 0 for x in range(0, threshold)}
solutions = []
for elf in range(1, threshold // 10):
    houses = [elf * x for x in range(1, 51)]
    for house in houses:
        current = presents[house]
        new = current + 11 * elf
        if new > threshold:
            solutions.append(house)
        presents[house] = new
print(f"Solution 2: {min(solutions)}")