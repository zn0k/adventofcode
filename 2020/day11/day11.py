from functools import partial

def get_start():
    with open("input.txt", "r") as f:
        return [[col for col in row] for row in f.readlines()]

def get_seat(s, r, c):
    return s[r][c] if 0 <= r < len(s) and 0 <= c < len(s[r]) else ""

def get_adj_seats(s, r, c):
    return [get_seat(s, r + d[0], c + d[1]) for d in dirs]

def get_first_vis_seat_in_dir(s, r, c, d):
    n = get_seat(s, r + d[0], c + d[1])
    return n if n != "." else get_first_vis_seat_in_dir(s, r + d[0], c + d[1], d)

def get_first_vis_seats(s, r, c):
    return [get_first_vis_seat_in_dir(s, r, c, d) for d in dirs]

def flip_seat(f, m, s, r, c):
    seat = get_seat(s, r, c)
    occ = f(s, r, c).count("#")
    if seat == "#" and occ >= m: return "L" 
    if seat == "L" and occ == 0: return "#" 
    return seat

dirs = [d for d in [(x, y) for x in [-1, 0, 1] for y in [-1, 0 , 1]] if d != (0,0)]
answer1 = partial(flip_seat, get_adj_seats, 4)
answer2 = partial(flip_seat, get_first_vis_seats, 5)
for f in [answer1, answer2]:
    s = get_start()
    while True:
        n = [[f(s, r, c) for c in range(0, len(s[r]))] for r in range(0, len(s))]
        if s == n:
            occ = sum(map(lambda x: x.count("#"), s))
            print(f"stable with {occ} seats occupied")
            break
        s = n