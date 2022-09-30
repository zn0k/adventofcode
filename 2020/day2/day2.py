with open("input.txt", "r") as f:
    lines = f.read().split("\n")


valid1 = 0
valid2 = 0
for line in lines:
    (freq, letter, pwd) = line.split(" ")
    (lower, upper) = freq.split("-")
    letter = letter.split(":")[0]
    occ = pwd.count(letter)
    if occ >= int(lower) and occ <= int(upper):
        valid1 += 1
    first = pwd[int(lower) - 1] == letter
    second = pwd[int(upper) - 1] == letter
    if (first or second) and (first != second):
        valid2 += 1

print("There are {0} valid passwords for scheme 1".format(valid1))
print("There are {0} valid passwords for scheme 2".format(valid2))
