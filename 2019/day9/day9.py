import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
 
from IntCode import IntCode

ic = IntCode(input_file="input.txt", input_values=[1], debug=True)
result = ic.run()
print(result)