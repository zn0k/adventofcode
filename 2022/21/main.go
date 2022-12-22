package main

import (
	"container/list"
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"strconv"
	"strings"
)

type Variable struct {
	Operands []string
	Operator string
}

func ReadInput(path string) (map[string]Variable, map[string]float64) {
	vars := make(map[string]Variable)
	vals := make(map[string]float64)
	buf, _ := ioutil.ReadFile(path)
	for _, line := range strings.Split(string(buf), "\n") {
		fields := strings.Fields(line)
		name := strings.TrimRight(fields[0], ":")
		switch len(fields) {
		case 2:
			val, _ := strconv.ParseInt(fields[1], 10, 64)
			vals[name] = float64(val)
		default:
			var v Variable
			v.Operands = []string{fields[1], fields[3]}
			v.Operator = fields[2]
			vars[name] = v
		}
	}
	return vars, vals
}

func SolveRoot(vars map[string]Variable, vals map[string]float64) float64 {
	// look at each variable starting at the root
	// if its components have been resolved, calculate it
	// if they haven't, add them to a FILO queue of variables to be resolved
	queue := list.New()
	queue.PushBack("root")
	current := queue.Front()
	for current != nil {
		name := current.Value.(string)
		if _, done := vals[name]; done { // already calculated this one
			queue.Remove(current)
			current = queue.Back()
		} else {
			v := vars[name]
			_, first := vals[v.Operands[0]]
			if !first {
				queue.PushBack(v.Operands[0]) // resolve the first component
			}
			_, second := vals[v.Operands[1]]
			if !second {
				queue.PushBack(v.Operands[1]) // resolve the second component
			}
			if first && second { // have both components, but need to calculate the value
				switch v.Operator {
				case "+":
					vals[name] = vals[v.Operands[0]] + vals[v.Operands[1]]
				case "-":
					vals[name] = vals[v.Operands[0]] - vals[v.Operands[1]]
				case "*":
					vals[name] = vals[v.Operands[0]] * vals[v.Operands[1]]
				case "/":
					vals[name] = vals[v.Operands[0]] / vals[v.Operands[1]]
				}
				queue.Remove(current)
			}
			current = queue.Back() // resolve queue from the back
		}
	}
	return vals["root"]
}

func main() {
	vars, originalVals := ReadInput(os.Args[1])
	vals := make(map[string]float64)
	for k, v := range originalVals {
		vals[k] = v
	}
	fmt.Printf("Solution 1: %d\n", int64(SolveRoot(vars, vals)))

	// use newton's method to find the root
	root := vars["root"]
	root.Operator = "-"
	// we're looking for root to evaluate to 0, at which point the two operands are equal
	vars["root"] = root
	// pick two starting values, the original one, and it doubled. this is arbitrary
	v1 := originalVals["humn"]
	v2 := v1 * 2
	var d1, d2 float64
	for {
		// make a copy of the values as they'll change each round
		vals := make(map[string]float64)
		for k, v := range originalVals {
			vals[k] = v
		}
		vals["humn"] = v1
		// solve for the first value, and record the different reported back
		d1 = SolveRoot(vars, vals)
		if d1 == 0 { // found a solution
			fmt.Printf("Solution 2: %d\n", int64(v1))
			break
		}

		// solve again for the second test value
		vals = make(map[string]float64)
		for k, v := range originalVals {
			vals[k] = v
		}
		vals["humn"] = v2
		d2 = SolveRoot(vars, vals)
		if d2 == 0 { // found a solution
			fmt.Printf("Solution 2: %d\n", int64(v2))
			break
		}

		// use newton's method to refine the guess for v1 or v2
		if math.Abs(d1) < math.Abs(d2) {
			v2 = v1 - (v2-v1)*d1/(d2-d1)
		} else {
			v1 = v2 - (v1-v2)*d2/(d1-d2)
		}
	}
}
