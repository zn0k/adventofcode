from functools import partial, lru_cache 

with open("input_test.txt", "r") as f:
    fish = [int(x) for x in f.readlines()[0].split(",")]

@lru_cache
def simulate_fish(days, age):
    if days <= 0:
        return 1
    if age == 0:
        return simulate_fish(days - 1, 6) + simulate_fish(days - 1, 8)
    else:
        return simulate_fish(days - 1, age - 1)

def solve(days):
    f = partial(simulate_fish, days)
    growth_rates = list(map(f, range(0, 7)))
    print(f"growth rates for {days} days is {growth_rates}")
    mapped = map(lambda x: growth_rates[x], fish)
    return sum(mapped)

print(f"Solution 1: {solve(80)}")
print(f"Solution 2: {solve(256)}")