with open("input.txt", "r") as f:
    words = [x.rstrip() for x in f.readlines()]

def test1(word):
    vowels = 0
    for vowel in "aeiou":
        vowels += word.count(vowel)
    if vowels >= 3:
        return True
    return False

def test2(word):
    for index in range(0, len(word) - 1):
        if word[index] == word[index + 1]:
            return True
    return False

def test3(word):
    for phrase in ["ab", "cd", "pq", "xy"]:
        if phrase in word:
            return False
    return True

nice = list(filter(lambda x: test1(x) and test2(x) and test3(x), words))

print(f"Solution 1: {len(nice)}")

def test4(word):
    for index in range(0, len(word) - 2):
        phrase = word[index:index + 2]
        if phrase in word[index + 2:]:
            return True
    return False

def test5(word):
    for index in range(0, len(word) - 2):
        if word[index] == word[index + 2]:
            return True
    return False    

nice = list(filter(lambda x: test4(x) and test5(x) , words))

print(f"Solution 2: {len(nice)}")
