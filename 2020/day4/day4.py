import functools

with open("input.txt", "r") as f:
    items = f.read().split("\n\n")
    passports = []
    for item in items:
        fields = item.replace("\n", " ").split(" ")
        passport = {}
        for field in fields:
            key, value = field.split(":")
            if key != "cid":
                passport[key] = value
        passports.append(passport)

required = sorted(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])

valid1 = filter(lambda x: required == sorted(x.keys()), passports)
print(len(valid1))


def validate_year(val, min, max):
    if int(val) >= min and int(val) <= max:
        return True
    return False

def validate_hgt(val):
    height = ""
    unit = ""
    for char in val:
        if char.isdigit():
            height += char
        else:
            unit += char
    height = int(height)
    if unit == "cm":
        if height >= 150 and height <= 193:
            return True
    elif unit == "in":
        if height >= 59 and height <= 76:
            return True
    return False

def validate_hcl(val):
    if val.startswith("#"):
        if len(val) == 7:
            val = val.replace("#", "")
            try:
                _ = int(val, 16)
                return True
            except:
                return False
    return False

def validate_ecl(val):
    if val in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        return True
    return False

def validate_pid(val):
    if len(val) == 9:
        try:
            _ = int(val)
            return True
        except:
            return False
    return False

def validate_passport(passport):
    return validate_year(passport["byr"], 1920, 2002) and \
           validate_year(passport["iyr"], 2010, 2020) and \
           validate_year(passport["eyr"], 2020, 2030) and \
           validate_hgt(passport["hgt"]) and \
           validate_hcl(passport["hcl"]) and \
           validate_ecl(passport["ecl"]) and \
           validate_pid(passport["pid"])

valid2 = filter(lambda x: validate_passport(x), valid1)
print(len(valid2))