#!/usr/bin/python3

def decode_entry(patterns, outputs):
   # Dictionary to translate between segment strings and numbers
   translatedict = {}

   # Easy digits (1,4,7,8) have a unique number of segments
   # Save 1 and 4 patterns for easier retrieval to figure out the harder ones
   for p in patterns:
      if len(p) == 2:
         translatedict[p] = 1
         one = p
      elif len(p) == 3:
         translatedict[p] = 7
      elif len(p) == 4:
         translatedict[p] = 4
         four = p
      elif len(p) == 7:
         translatedict[p] = 8

   # Harder digits need length plus comparison to a known digit to figure out
   for p in patterns:
      if len(p) == 5:
         # 3 is only length 5 digit with both segments from 1
         if len(set(one).intersection(p)) == 2:
            translatedict[p] = 3
         # 2 is only length 5 digit with 2 segments from 4
         elif len(set(four).intersection(p)) == 2:
            translatedict[p] = 2
         else:
            translatedict[p] = 5
      if len(p) == 6:
         # 9 is only length 6 digit with all four segments from 4
         if len(set(four).intersection(p)) == 4:
            translatedict[p] = 9
         # with 9 gone, 0 is only length 6 digit with both segments from 1
         elif len(set(one).intersection(p)) == 2:
            translatedict[p] = 0
         else:
            translatedict[p] = 6

   digitstring = ''
   for o in outputs:
      digitstring += str(translatedict[o])
   return int(digitstring)

# Read input file and sort strings to make matching easier
inputlist = []
with open("8-100000.in", "r") as inputfile:
   for line in inputfile:
      patterns, output = line.rstrip().split('|')
      inputlist.append([ [''.join(sorted(p)) for p in patterns.split()],
                         [''.join(sorted(p)) for p in output.split()] ])
# Part 1
easydigits = 0
for e in inputlist:
   for o in e[1]:
      if len(o) == 2 or len(o) == 3 or len(o) == 4 or len(o) == 7:
         easydigits += 1
print('Outputs with a unique number of segments was', easydigits)

# Part 2
total = 0
for l in inputlist:
   total += decode_entry(l[0], l[1])
print('Sum of all outputs is', total)
