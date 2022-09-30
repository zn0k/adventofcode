from itertools import cycle, product
from functools import lru_cache

def move(position, score, roll):
    position = (position + roll - 1) % 10 + 1
    return (position, score + position)

def part1(player1, player2):
    state = [(player1, 0), (player2, 0)]
    die = cycle(range(1, 101))
    rolls = 0
    while True:
        for index, player in enumerate(state):
            position, score = player
            roll = next(die) + next(die) + next(die)
            rolls += 3
            position, score = state[index] = move(position, score, roll)
            if score >= 1000:
                _, lower_score = state[1 - index]
                return rolls * lower_score

def part2(player1, player2):
    @lru_cache(maxsize=None)
    def count_wins(player1, player2):
        wins1 = wins2 = 0
        for x, y, z in product([1,2,3], repeat=3):
            position1, score1 = player1
            result = move(position1, score1, x + y + z)
            if result[1] >= 21:
                wins1 += 1
            else:
                nextwins2, nextwins1 = count_wins(player2, result)
                wins1 += nextwins1
                wins2 += nextwins2
        return wins1, wins2
    
    return max(count_wins((player1, 0), (player2, 0)))

print(f"Solution 1: {part1(9, 4)}")
print(f"Solution 2: {part2(9, 4)}")