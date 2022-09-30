weapons = [(8, 4, 0), (10, 5, 0), (25, 6, 0), (40, 7, 0), (74, 8, 0)]
armors = [(0, 0, 0), (13, 0, 1), (31, 0, 2), (53, 0, 3), (75, 0, 4), (102, 0, 5)]
rings = [(0, 0, 0), (25, 1, 0), (50, 2, 0), (100, 3, 0), (20, 0, 1), (40, 0, 2), (80, 0, 3)]

boss = (109, 8, 2)

def attack(attacker, defender):
    damage = attacker[1] - defender[2]
    if damage < 1:
        damage = 1
    return (defender[0] - damage, defender[1], defender[2])

def turn(player, boss):
    boss = attack(player, boss)
    player = attack(boss, player)
    return (player, boss)

def fight(player, boss):
    while True:
        player, boss = turn(player, boss)
        if boss[0] <= 0:
            return True
        if player[0] <= 0:
            return False

def modify_player(player, modifiers):
    return (player[0], player[1] + modifiers[1], player[2] + modifiers[2])

base_player = (100, 0, 0)

win_costs = []
loss_costs = []
for weapon in weapons:
    cost_with_weapon = weapon[0]
    player_with_weapon = modify_player(base_player, weapon)
    for armor in armors:
        cost_with_armor = cost_with_weapon + armor[0] 
        player_with_armor = modify_player(player_with_weapon, armor)
        for ring in rings:
            cost_with_ring = cost_with_armor + ring[0]
            player_with_one_ring = modify_player(player_with_armor, ring)
            for second_ring in rings:
                if second_ring == ring:
                    continue
                cost_with_two_rings = cost_with_ring + second_ring[0]
                player_with_two_rings = modify_player(player_with_one_ring, second_ring)
                if fight(player_with_two_rings, boss):
                    win_costs.append(cost_with_two_rings)
                else:
                    loss_costs.append(cost_with_two_rings)

print(f"Solution 1: {min(win_costs)}")
print(f"Solution 2: {max(loss_costs)}")