with open("input.txt", "r") as f:
    replacements = {}
    for line in [x.rstrip() for x in f.readlines()]:
        if not len(line):
            continue
        if " => " in line:
            left, right = line.split(" => ")
            if left in replacements:
                replacements[left].append(right)
            else:
                replacements[left] = [right]
        else:
            medicine = line

def generate(molecule, replacements):
    results = set()
    for key in replacements:
        for variant in replacements[key]:
            start = 0
            index = molecule.find(key, start)
            while index != -1:
                result = molecule[0:index] + molecule[index:].replace(key, variant, 1)
                results.add(result)
                index = molecule.find(key, index + 1)
    return results

molecules = generate(medicine, replacements)
print(f"Solution 1: {len(molecules)}")

reverse = {}
for key in replacements:
    for variant in replacements[key]:
        if variant in reverse:
            print("duplicate")
        else:
            reverse[variant] = key

total_molecules = len(list(filter(lambda x: x.isupper(), [c for c in medicine])))
rns = medicine.count("Rn")
ars = medicine.count("Ar")
ys = medicine.count("Y")
steps = total_molecules - rns - ars - 2 * ys - 1
print(f"Solution 2: {steps}")