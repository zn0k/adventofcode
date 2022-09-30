import copy
#with open('15_test_input.txt','r') as fd:
with open('input.txt', 'r') as fd:
    input_vals = [int(x) for x in fd.readline().split(',')]
def nth_number_spoken(vals, n):
    vals = copy.deepcopy(vals)
    while len(vals) < n:
        last = vals[-1]
        rest = vals[:-1]
        if last not in rest:
            vals.append(0)
            continue
        vals.append(list(reversed(rest)).index(last) + 1)
    return vals[-1]
print(nth_number_spoken(input_vals, 2020))
# 614
def better_nth_number_spoken(vals, n):
    last_occurrences = {val:i for i, val in enumerate(vals[:-1])}
    i = len(vals) - 1
    curr = vals[-1]
    while i < n-1:
        if curr not in last_occurrences:
            last_occurrences[curr] = i
            curr = 0
            i += 1
            continue
        soon = i - last_occurrences[curr]
        last_occurrences[curr] = i
        curr = soon
        i += 1
    return curr
print(better_nth_number_spoken(input_vals, 30000000))
# 1065
# about 10 seconds run time
