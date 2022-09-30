with open("input.txt", "r") as f:
    data = {}
    for line in f.read().split("\n"):
        container, content = line.split(" bags contain ")
        data[container] = []
        for item in content.rstrip(".").split(", "):
            item = item.replace(" bags", "").replace(" bag", "")
            quantity = item.split(" ")[0]
            if not quantity == "no":
                item = " ".join(item.split(" ")[1::])
                data[container].append({"name": item, "quantity": int(quantity)})

def filter_containers(name):
    result = []
    for key, value in data.items():
        for contained in value:
            if contained["name"] == name:
                result.extend([key, *filter_containers(key)])
    return result

result = set(filter_containers("shiny gold"))
print(f"part 1: {len(result)}")

def count_contained(name):
    total = 0
    for item in data[name]:
        total += item["quantity"]
        total += item["quantity"] * count_contained(item["name"])
    return total

result = count_contained("shiny gold")
print(f"part 2: {result}")