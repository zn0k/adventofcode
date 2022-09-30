#!/usr/bin/env python


with open("input.txt", "r") as f:
    numbers = f.read().split("\n")


done = False
for number1 in numbers:
    for number2 in numbers:
        if int(number1) + int(number2) == 2020:
            print(int(number1) * int(number2))
            done = True
            break
    if done:
        break
            
done = False
for number1 in numbers:
    for number2 in numbers:
        for number3 in numbers:
            if int(number1) + int(number2) + int(number3) == 2020:
                print(int(number1) * int(number2) * int(number3))
                done = True
                break
        if done:
            break
    if done:
        break