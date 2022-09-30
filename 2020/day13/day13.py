with open("input.txt", "r") as f:
    lines = f.readlines()
    earliest = int(lines[0].replace("\n", ""))
    valid = [int(x) for x in lines[1].split(",") if x != "x"]
    buses = [(i, int(x)) for i, x in enumerate(lines[1].split(",")) if x != "x"]

leave_times = map(lambda x: x * (int(earliest / x) + 1), valid)
wait_times = list(map(lambda x: x - earliest, leave_times))
best = min(wait_times)
best_line = valid[wait_times.index(best)]
print(f"answer 1: {best * best_line}")

skip = buses[0][1]
t = buses[0][1]
counter = 0
for pos, bus_id in buses[1::]:
    while ((t + pos) % bus_id) != 0:
        t += skip
        counter += 1
    skip *= bus_id
print(f"answer 2 is {t}, took {counter} loops")