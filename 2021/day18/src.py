import ast
from math import ceil, floor
from functools import reduce
from itertools import combinations

class Node:
    def __init__(self, parent):
        self.parent = parent
        self.left = None
        self.right = None
    
    def magnitude(self):
        return self.left.magnitude() * 3 + self.right.magnitude() * 2
    
    def __str__(self):
        return "[" + str(self.left) + "," + str(self.right) + "]"

class Value:
    def __init__(self, parent, value):
        self.value = value
        self.parent = parent

    def magnitude(self):
        return self.value

    def __str__(self):
        return str(self.value)

def parse(number):
    def to_node(parent, left, right):
        node = Node(parent)
        node.left = to_node(node, left[0], left[1]) if isinstance(left, list) else Value(node, left)
        node.right = to_node(node, right[0], right[1]) if isinstance(right, list) else Value(node, right)        
        return node
    parsed = ast.literal_eval(number)
    return to_node(None, parsed[0], parsed[1])

def traverse(node):
    return [node] if isinstance(node, Value) else traverse(node.left) + traverse(node.right)

def reduce_number(root):
    def get_level(item):
        level = 0
        while not item.parent is None:
            level += 1
            item = item.parent
        return level

    exploded, split = True, True
    while exploded or split:
        ordered = traverse(root)
        exploded, split = False, False
        for index, value in enumerate(ordered):
            level = get_level(value)
            if level == 5:
                if index != 0:
                    ordered[index - 1].value += value.value
                if index < len(ordered) - 2:
                    ordered[index + 2].value += ordered[index + 1].value
                if value.parent.parent.left is value.parent:
                    value.parent.parent.left = Value(value.parent.parent, 0)
                else:
                    value.parent.parent.right = Value(value.parent.parent, 0)
                exploded = True
                break
        if exploded: continue
        for value in ordered:
            if value.value >= 10:
                node = Node(value.parent)
                node.left = Value(node, floor(value.value / 2))
                node.right = Value(node, ceil(value.value / 2))
                if value.parent.left is value:
                    value.parent.left = node
                else:
                    value.parent.right = node
                split = True
                break
    return root

def add(left, right):
    node = Node(None)
    left.parent = node
    right.parent = node
    node.left = left
    node.right = right
    return reduce_number(node)

with open("input.txt", "r") as f:
    numbers = [l.rstrip() for l in f]

reduced = reduce(add, map(parse, numbers))
print(f"Solution 1: {reduced.magnitude()}")

def max_sum_pair(left, right):
    x, y = parse(left), parse(right)
    xy = add(x, y).magnitude()
    x, y = parse(left), parse(right)
    yx = add(y, x).magnitude()
    return max([xy, yx])

sums = map(lambda x: max_sum_pair(x[0], x[1]), combinations(numbers, 2))
print(f"Solution 2: {max(sums)}")