import networkx as nx
from functools import reduce

with open("input.txt", "r") as f:
    board = [[int(x) for x in l.rstrip()] for l in f]

directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def get_neighbors(x, y, max_x, max_y):
    return [(x + o_x, y + o_y) for o_x, o_y in directions if 0 <= x + o_x < max_x and 0 <= y + o_y < max_y]

def bottom_right(board):
    return (len(board[0]) - 1, len(board) - 1)

def build_graph(board):
    max_x = len(board[0])
    max_y = len(board)
    G = nx.DiGraph()
    for y in range(max_y):
        for x in range(max_x):
            for n_x, n_y in get_neighbors(x, y, max_x, max_y):
                G.add_edge((x, y), (n_x, n_y), weight=board[n_y][n_x])
    return G

def sum_path(G, path):
    return sum(map(lambda x: G.edges[(x[0], x[1])]["weight"], zip(path, path[1:])))

def get_risk(board):
    G = build_graph(board)
    return sum_path(G, list(nx.dijkstra_path(G, source=(0,0), target=bottom_right(board))))

print(f"Solution 1: {get_risk(board)}")

def print_board(board):
    for row in board:
        print("".join(map(str, row)))

def expand_board(board):
    def inc_row(r, i):
        return [x + i - (9 * ((x + i) // 10)) for x in r]
    def inc_tile(t, i):
        return [inc_row(r, i) for r in t]        
    def build_row(r):
        return reduce(lambda x, y: x + inc_row(r, y), range(5), [])
    base = [build_row(r) for r in board]
    result = base
    for i in range(4):
        base = inc_tile(base, 1)
        result += base
    return result

board = expand_board(board)
print(f"Solution 2: {get_risk(board)}")
