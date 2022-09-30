from collections import deque
input = "389125467"
input = "157623984"
input = [int(x) for x in input]
rounds = 100
cups = deque(input)
for r in range(0, rounds):
    # get the current cup
    current = cups.popleft()
    # get the next three cups
    next_three = [cups.popleft(), cups.popleft(), cups.popleft()]
    # put the current cup back
    cups.appendleft(current)
    # find the destination cup
    destination = (current - 1) if (current - 1 > 0) else 9
    while destination in next_three:
        destination -= 1
        if destination <= 0: destination = 9
    # insert the next three cups back in
    for x in reversed(next_three):
        cups.insert(cups.index(destination) + 1, x)
    # slide the whole data structure one to the right
    cups.rotate(-1)
# slide the data structure until cup 1 is at the start
while cups[0] != 1:
    cups.rotate(-1)
# remove it
one = cups.popleft()
# stringify the rest
answer1 = "".join([str(x) for x in cups])
print(f"Answer 1: {answer1}")
# oh how proud i was of using deque that way. so elegant, so fast.
# but does it scale to 10m operations on 1m element lists? hell no.
# how do you do linked lists in python? google says deque. it ain't, really.
# oh well. make one using a dictionary
# each key simply points to the next key
# first, populate from the input, pointing each at the next value
cups = {input[i]: input[i + 1] for i in range(0, len(input) - 1)}
# then point the last input element to the max value + 1
cups[input[-1]] = max(input) + 1
# then fill up to a million with sequential elements
max_fill = 1_000_000
cups.update({x: x + 1 for x in range(max(input) + 1, max_fill)})
# then point the max fill value back to the beginning
cups[max_fill] = input[0]

# prepare a list where the item at index i points to the next item
cups = list(range(0, len(input) + 1))
# go through the input except for its last member and insert them into the data structure
for i in range(0, len(input) - 1):
    cups[input[i]] = cups[input[i + 1]]
# point the last input value to the max of the input + 1
n = max(input) + 1
cups[input[-1]] = n
# fill it up to a million
while n <= max_fill:
    n += 1
    cups.append(n)
# and point the last item back to the beginning
cups.append(1)

rounds = 10_000_000
current = input[0]
for r in range(0, rounds):
    # get the next three
    next_three = [cups[current]]
    next_three.append(cups[next_three[0]])
    next_three.append(cups[next_three[1]])
    # get the destination
    destination = (current - 1) if (current - 1 > 0) else max_fill
    while destination in next_three:
        destination -= 1
        if destination <= 0: destination = max_fill
    # re-point current to what the last cup in the next three points to
    # this cuts those three cups out of the looping sequence
    cups[current] = cups[next_three[2]]
    # re-point the last cup in the next three to what the destinaton points to
    # this inserts the end of the sequence consisting of the next three cups
    cups[next_three[2]] = cups[destination]
    # re-point the destination to the first of the next three cups
    # this inserts the start of the sequence consisting of the next three cups
    cups[destination] = next_three[0]
    # slide over to the next cup
    current = cups[current]
a = cups[1]
b = cups[a]
print(f"Answer 2: {a * b}")