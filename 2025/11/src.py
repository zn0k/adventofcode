#!/usr/bin/env python3

import sys
import networkx as nx

devices = {}
with open(sys.argv[1], "r") as f:
    for line in f.readlines():
        k, vs = line.strip().split(": ")
        devices[k] = vs.split(" ")

G = nx.DiGraph()
for device, connections in devices.items():
    for target in connections:
        G.add_edge(device, target)

solution1 = len(list(nx.all_simple_paths(G, "you", "out")))
print(f"Solution 1: {solution1}")

# paths = nx.all_simple_paths(G, "svr", "out")
# solution2 = len([p for p in paths if "fft" in p and "dac" in p])
# print(f"Solution 2: {solution2}")
# this runs too slow, break it up into sub-problems

# use dynamic programming to count paths between source and target
def count_paths(G, s, t):
    # get the graph topology
    topology = list(nx.topological_sort(G))
    # start a dictionary to count the number of paths
    # to get to a given node
    paths = {node: 0 for node in topology}
    # seed it by setting the ways to get to the source to 1
    paths[s] = 1

    # walk the nodes in the topology
    for u in topology:
        # walk the nodes that we can get to from the current node
        for v in G.successors(u):
            # and propagate the number of ways to get there
            paths[v] += paths[u]
    
    return paths[t]

# break down the path from svr to out via the two waypoints
# we can either go through dac first, or through fft
dac_fft = [("svr", "dac"), ("dac", "fft"), ("fft", "out")]
fft_dac = [("svr", "fft"), ("fft", "dac"), ("dac", "out")]

solution2 = 0
# walk the options
for ps in [dac_fft, fft_dac]:
    option = 1
    # walk the segments
    for u, v in ps:
        # sub-solution is the product of paths between segments
        option *= count_paths(G, u, v)
    # puzzle solution is the sum of the paths of the options
    solution2 += option

print(f"Solution 2: {solution2}")