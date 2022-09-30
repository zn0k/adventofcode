pwd = "vzbxkghb"

def increase(s):
    start, last = s[:-1], s[-1:]
    last = chr(ord(last) + 1)
    if last > 'z':
        last = 'a'
        start = increase(start)
    return start + last

def test1(s):
    letters = {x: 1 for x in s}
    letters = list(letters.keys())
    for letter in letters:
        if letter > 'x':
            continue
        fragment = letter + increase(letter)
        fragment += increase(fragment[1])
        if fragment in s:
            return True
    return False

def test2(s):
    for letter in "iol":
        if letter in s:
            return False
    return True

def test3(s):
    letters = {x: 1 for x in s}
    letters = list(letters.keys())
    doubles = 0
    for letter in letters:
        fragment = letter + letter
        if fragment in s:
            doubles += 1
    if doubles >= 2:
        return True
    return False

while True:
    pwd = increase(pwd)
    if test2(pwd) and test1(pwd) and test3(pwd):
        break

print(f"Solution 1: {pwd}")

while True:
    pwd = increase(pwd)
    if test2(pwd) and test1(pwd) and test3(pwd):
        break

print(f"Solution 2: {pwd}")