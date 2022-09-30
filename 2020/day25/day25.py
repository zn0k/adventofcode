with open("input.txt", "r") as f:
    door_pub, key_pub = [int(x) for x in f.readlines()]

def crack(pub):
    r = 0
    val = 1
    sub = 7
    while True:
        r += 1
        val = (val * sub) % 20201227
        if val == pub:
            break
    return r

def transform(sub, rounds):
    val = 1
    for _ in range(rounds):
        val = (val * sub) % 20201227
    return val

door_rounds = crack(door_pub)
print(f"Door rounds is {door_rounds}")
key_rounds = crack(key_pub)
print(f"Door rounds is {key_rounds}")

key = transform(door_pub, key_rounds)
print(f"Answer 1: {key}")