from functools import reduce
from itertools import permutations
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
 
from IntCode import IntCode

def run_sequence(seq):
    output = 0
    for amp_input in seq:
        ic = IntCode(input_file="input.txt", input_values=[amp_input, output])
        output = ic.run()[0]
    return (output, seq)

perms = permutations(tuple(range(0,5)), 5)
outputs = map(run_sequence, perms)
highest = reduce(lambda x, y: x if x[0] > y[0] else y, outputs)
print(f"Answer 1: {highest}")

def run_feedback_sequence(seq):
    input_file = "input.txt"
    amps = []
    amps.append(IntCode(input_file=input_file, input_values=[seq[0], 0], single_step_output=True))
    output = amps[0].run()
    amps.append(IntCode(input_file=input_file, input_values=[seq[1], output], single_step_output=True))
    output = amps[1].run()
    amps.append(IntCode(input_file=input_file, input_values=[seq[2], output], single_step_output=True))
    output = amps[2].run()
    amps.append(IntCode(input_file=input_file, input_values=[seq[3], output], single_step_output=True))
    output = amps[3].run()
    amps.append(IntCode(input_file=input_file, input_values=[seq[4], output], single_step_output=True))
    output = amps[4].run()
    while not amps[4].terminated:
        for i in range(0, 5):
            output = amps[i].run(input_values=[output])
    return (output, seq)

perms = permutations(tuple(range(5, 10)), 5)
outputs = map(run_feedback_sequence, perms)
highest = reduce(lambda x, y: x if x[0] > y[0] else y, outputs)
print(f"Answer 2: {highest}")