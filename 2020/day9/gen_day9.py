import random

values = []
initial = set(range(1, 51))
for i in range(0, 26):
    new = random.choice(list(initial))
    initial.remove(new)
    values.append(new)

for i in range(0, 976):
    keys = list(set(values[-25::]))
    a = random.choice(keys)
    keys.remove(a)
    values.append(a + min(keys))

len_seq = random.randint(15, 25)
seq_start = random.randint(500, 900)
seq = values[seq_start:seq_start+len_seq]
weakness = min(seq) + max(seq)
vuln = sum(seq)

patch_index = 0
for i in range(seq_start + len_seq + 1, 1001):
    if values[i] > vuln:
        patch_index = i
        break
    i += 1

values[patch_index] = vuln

print(f"Answer 1: {vuln}")
print(f"Answer 2: {weakness}")
print(f"{values}")