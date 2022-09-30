from functools import partial, reduce
from operator import add, mul

with open("input.txt", "r") as f:
    problems = [x.replace(")", " )").replace("(", "( ").rstrip().split(" ") for x in f.readlines()]
    problems = [[y if y in "+*()" else int(y) for y in x] for x in problems]

def basic_case_no_precedence(problem):
    left = problem[0]
    for element in problem[1::]:
        if element == "+":
            f = partial(add, left)
        elif element == "*":
            f = partial(mul, left)
        else:
            left = f(element)
    return left

def solve(problem, basic_solver):
    def split_problem(p, c):
        index = problem.index(c)
        return (problem[0:index], problem[index + 1::])

    if "(" in problem:
        left, right = split_problem(problem, "(")
        partial, right = solve(right, basic_solver)
        problem = left + [partial] + right
    if ")" in problem:
        left, right = split_problem(problem, ")")
        return (basic_solver(left), right)
    return basic_solver(problem)

answers = [solve(p, basic_case_no_precedence) for p in problems]
print(f"Answer 1: {sum(answers)}")

def basic_case_addition_precedence(problem):
    def get_left(p):
        index = p.index("+") 
        return ([], p[0]) if index == 1 else (p[0:index - 1], p[index - 1])

    def get_right(p):
        index = p.index("+")
        return ([], p[-1]) if len(p) - index == 2 else (p[index + 2::], p[index + 1])

    while "+" in problem:
        left, left_operand = get_left(problem)
        right, right_operand = get_right(problem)
        problem = left + [left_operand + right_operand] + right
    return reduce(mul, filter(lambda x: x != "*", problem))

answers = [solve(p, basic_case_addition_precedence) for p in problems]
print(f"Answer 2: {sum(answers)}")