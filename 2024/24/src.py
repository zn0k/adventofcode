#!/usr/bin/env python3

import sys
import networkx as nx
from functools import partial
from itertools import chain
from collections import Counter

with open(sys.argv[1], "r") as f: 
  chunks = f.read().split("\n\n")
  
vals = {
  k: 1 if v == "1" else 0
  for k, v in [l.split(": ") for l in chunks[0].split("\n")]
}

rules = {}
for line in chunks[1].split("\n"):
  fields = line.split(" ")
  rules[fields[4]] = (fields[0], fields[1], fields[2])

def evaluate(vals, rules, x):
  if x not in vals:
    rule = rules[x]
    match rule[1]:
      case "AND":
        result = evaluate(vals, rules, rule[0]) & evaluate(vals, rules, rule[2])
      case "OR":
        result = evaluate(vals, rules, rule[0]) | evaluate(vals, rules, rule[2])
      case "XOR":
        result = evaluate(vals, rules, rule[0]) ^ evaluate(vals, rules, rule[2])
    vals[x] = result
  else:
    result = vals[x]
  return result

def bin2dec(vals, rules, x):
  f = partial(evaluate, vals, rules)
  r = "".join(map(str, reversed(list(map(f, x)))))
  return int(r, 2)

outputs = sorted(x for x in rules.keys() if x.startswith("z"))
part1 = bin2dec(vals, rules, outputs)
print(f"Solution 1: {part1}")

problems = set()

# pull out all the gates as tuples (output, input, input)
gates = [(k, v[0], v[2]) for k, v in rules.items()]
xors = [(k, v[0], v[2]) for k, v in rules.items() if v[1] == "XOR"]
ors = [(k, v[0], v[2]) for k, v in rules.items() if v[1] == "AND"]
ands = [(k, v[0], v[2]) for k, v in rules.items() if v[1] == "OR"]

xor_outputs = set(x[0] for x in xors)
or_outputs = set(x[0] for x in ors)
and_outputs = set(x[0] for x in ands)

xor_inputs = set(x for i in xors for x in i[1:3])
or_inputs = set(x for i in ors for x in i[1:3])
and_inputs = set(x for i in ands for x in i[1:3])

G = nx.DiGraph()
for x in xors:
  G.add_node(x, color="blue", type="xor")
for x in ands:
  G.add_node(x, color="red", type="and")
for x in ors:
  G.add_node(x, color="green", type="or")

for x in chain(xors, ands, ors):
  out, in1, in2 = x
  ps = [g for g in gates if in1 == g[0] or in2 == g[0]]
  for p in ps:
    G.add_edge(p, x)
  cs = [g for g in gates if out in g[1:3]]
  for c in cs:
    G.add_edge(x, c)

# render graph to a dot file so we can draw it with graphviz
nx.drawing.nx_pydot.write_dot(G, "graph.dot")
# that informs the logic below

# check all the XOR gates
for gate in xors:
  out, in1, in2 = gate
  # first type of XOR gate is a system output
  if out[0] == "z":
    # our inputs should be a XOR gate and an AND gate
    ps = set(G.predecessors(gate))
    p_types = [G.nodes[p]["type"] for p in ps]
    if any(p == "xor" for p in p_types) and any(p == "and" for p in p_types):
      continue
  # other type of XOR gate takes two system inputs
  if set([in1[0], in2[0]]) == set(["x", "y"]):
    # outputs should be an OR gate and a XOR gate
    cs = set(G.successors(gate))
    c_types = [G.nodes[c]["type"] for c in cs]
    if any(c == "xor" for c in c_types) and any(c == "or" for c in c_types):
      continue
  # gate is problematic
  problems.add(gate)

# check all the AND gates
for gate in ands:
  out, in1, in2 = gate
  # AND gates have two OR gates as inputs
  ps = set(G.predecessors(gate))
  p_types = [G.nodes[p]["type"] for p in ps]
  if all(p == "or" for p in p_types):
    # and they should have outputs to an OR gate and a XOR gate
    cs = set(G.successors(gate))
    c_types = [G.nodes[c]["type"] for c in cs]
    if set(c_types) == set(["or", "xor"]):
      continue
  problems.add(gate)

# check all the OR gates
for gate in ors:
  out, in1, in2 = gate
  cs = set(G.successors(gate))
  c_types = [G.nodes[c]["type"] for c in cs]
  # first type of OR gate takes two system inputs
  if set([in1[0], in2[0]]) == set(["x", "y"]):
    # output should be a single AND gate
    if len(cs) == 1 and all(c == "and" for c in c_types):
      continue
  # the other type takes an AND gate and a XOR gate
  ps = set(G.predecessors(gate))
  p_types = [G.nodes[p]["type"] for p in ps]
  if any(p == "xor" for p in p_types) and any(p == "and" for p in p_types):
    # output should be to a single and gate
    if len(cs) == 1 and all(c == "and" for c in c_types):
      continue
  problems.add(gate)

# z00, z01, and z45 don't find the pattern
for g in [g for g in gates if g[0] in ["z00", "z01", "z45"]]:
  problems.remove(g)

wires = [w for p in problems for w in p]
c = Counter(wires)
print(c)

# found via visaul inspection of the PDF based on the outpiut of the counter
part2 = "jgb,rkf,rrs,rvc,vcg,z09,z20,z24"
          
print(f"Solution 2: {part2}")
