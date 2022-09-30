with open("input.txt", "r") as f:
    lines = f.read().split("\n")

def decode(start, rest, lower_char):
    if rest == "":
        return start
    else:
        if rest[0] == lower_char:
            return decode(start, rest[1::], lower_char)
        else:
            return decode(start + (2 ** len(rest[1::])), rest[1::], lower_char)

def get_seatID(boarding_pass):
    row = decode(0, boarding_pass[0:7], "F")
    col = decode(0, boarding_pass[7::], "L")
    return row * 8 + col

seat_ids = list(map(get_seatID, lines))
print("highest seat ID is {0}".format(max(seat_ids)))

def find_missing(remaining):
    candidate = remaining[0] + 1
    if candidate == remaining[1]:
        return find_missing(remaining[1::])
    else:
        return candidate

print("missing seat ID is {0}".format(find_missing(sorted(seat_ids))))
    