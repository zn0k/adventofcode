from pathlib import Path
i = Path("input.txt").read_text()
for l in [4, 14]:
    print(i.index(''.join(list(filter(lambda x: len(set(x)) == len(x), zip(*[i[x:] for x in range(l)])))[0]))+l)