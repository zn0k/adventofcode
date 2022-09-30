import networkx as nx
from typing import NamedTuple

# class for a point so we can access the x and y attributes by name
class Point(NamedTuple):
    x: int
    y: int

# get the start and the end of a line as a list of points
def get_line(line):
    def make_point(p):
        x, y = p.split(",")
        return Point(int(x), int(y))
    return [make_point(p) for p in line.rstrip().replace(" -> ", ";").split(";")]

with open("input.txt", "r") as f:
    lines = [get_line(l) for l in f]

# generator for all points on a given line
# returns tuples, consisting of the point and 
# whether or not the point is on a diagonal
def get_line_points(line):
    p1, p2 = line
    x_step = 1 if p1.x < p2.x else -1
    y_step = 1 if p1.y < p2.y else -1
    horizontals = range(p1.x, p2.x + x_step, x_step)
    verticals = range(p1.y, p2.y + y_step, y_step)
    if p1.x == p2.x:
        for y in verticals:
            yield (Point(p1.x, y), False)
    elif p1.y == p2.y:
        for x in horizontals:
            yield (Point(x, p1.y), False)
    else:
        # diagonal line
        for point in zip(horizontals, verticals):
            yield (Point(point[0], point[1]), True)

# initialize a graph with the capacity for parallel edges
G = nx.MultiGraph()
for line in lines:
    for point, on_diagonal in get_line_points(line):
        # add an edge to the graph for each point on the line
        # this automagically adds vertices not yet present
        G.add_edge(point, point, on_diagonal=on_diagonal)
 
# count the vertices with more than two edges
# also take in an optional filter for edges
def count_solutions(graph, edge_filter=None):
    def count_edges(node):
        edges = graph.edges(node, data=True)
        if edge_filter: edges = list(filter(edge_filter, edges))
        return len(edges)
    counts = map(count_edges, graph.nodes())
    return len(list(filter(lambda x: x >= 2, counts)))

# build an edge filter that discards edges that are on diagonal lines
edge_filter = lambda x: not x[2]["on_diagonal"]
print(f"Solution 1: {count_solutions(G, edge_filter=edge_filter)}")
print(f"Solution 2: {count_solutions(G)}")