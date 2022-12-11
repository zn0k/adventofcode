package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"strconv"
	"strings"
)

const (
	_ = iota
	SELF
	CONSTANT
	ADD
	MULTIPLY
)

type Test struct {
	Divisor int
	True    int
	False   int
}

func (t *Test) Eval(n int) int {
	if n%t.Divisor == 0 {
		//fmt.Printf("    Current worry level is divisible by %d.\n", t.Divisor)
		return t.True
	} else {
		//fmt.Printf("    Current worry level is not divisible by %d.\n", t.Divisor)
		return t.False
	}
}

type Operation struct {
	Operator    int
	OperandType int
	Operand     int
}

func (o *Operation) Eval(n int) int {
	//fmt.Printf("    Worry level")
	operand := 0
	result := 0
	switch o.OperandType {
	case CONSTANT:
		operand = o.Operand
	default:
		operand = n
	}

	switch o.Operator {
	case ADD:
		result = n + operand
		//fmt.Printf(" increases by %d to", operand)
	default:
		result = n * operand
		//fmt.Printf(" is multiplied by %d to", operand)
	}
	//fmt.Printf(" %d.\n", result)
	return result
}

type Monkey struct {
	Items       []int
	Operation   Operation
	Test        Test
	Inspections int
}

func NewMonkey(o Operation, t Test) *Monkey {
	m := &Monkey{Operation: o, Test: t, Inspections: 0}
	m.Items = make([]int, 0)
	return m
}

type Pack struct {
	Monkeys       []*Monkey
	DecreaseWorry bool
}

func NewPack() *Pack {
	p := &Pack{DecreaseWorry: true}
	p.Monkeys = make([]*Monkey, 0)
	return p
}

func (p *Pack) PlayRound() {
	for _, m := range p.Monkeys {
		//fmt.Printf("Monkey %d:\n", i)
		for _, item := range m.Items {
			//fmt.Printf("  Monkey inspects an item with worry level of %d.\n", item)
			new := m.Operation.Eval(item)
			if p.DecreaseWorry {
				new /= 3
			}
			//fmt.Printf("    Monkey gets bored with item. Worry level is divided by 3 to %d.\n", new)
			to := m.Test.Eval(new)
			//fmt.Printf("    Item with worry level %d is thrown to monkey %d.\n", new, to)
			p.Monkeys[to].Items = append(p.Monkeys[to].Items, new)
			m.Inspections += 1
		}
		m.Items = []int{}
	}
}

func (p *Pack) Print() {
	for i, m := range p.Monkeys {
		fmt.Printf("Monkey %d: %v\n", i, m.Items)
	}
}

func (p *Pack) PrintInspections() {
	for i, m := range p.Monkeys {
		fmt.Printf("Monkey %d: %d\n", i, m.Inspections)
	}
}

func (p *Pack) MostActive() int {
	var inspections []int

	for _, m := range p.Monkeys {
		inspections = append(inspections, m.Inspections)
	}

	sort.Ints(inspections)
	return inspections[len(inspections)-2] * inspections[len(inspections)-1]
}

func ReadInput(path string) *Pack {
	buf, err := ioutil.ReadFile(path)
	if err != nil {
		panic(fmt.Sprintf("unable to read %s", path))
	}
	pack := NewPack()

	for _, chunk := range strings.Split(string(buf), "\n\n") {
		lines := strings.Split(chunk, "\n")

		fields := strings.Fields(lines[3])
		testDivisor, _ := strconv.Atoi(fields[3])
		fields = strings.Fields(lines[4])
		testTrue, _ := strconv.Atoi(fields[5])
		fields = strings.Fields(lines[5])
		testFalse, _ := strconv.Atoi(fields[5])
		test := Test{Divisor: testDivisor, True: testTrue, False: testFalse}

		var operation Operation
		fields = strings.Fields(lines[2])
		switch fields[4] {
		case "*":
			operation.Operator = MULTIPLY
		case "+":
			operation.Operator = ADD
		}
		switch fields[5] {
		case "old":
			operation.OperandType = SELF
		default:
			operation.OperandType = CONSTANT
			i, _ := strconv.Atoi(fields[5])
			operation.Operand = i
		}

		fields = strings.Fields(lines[1])
		item_fields := strings.Split(strings.Join(fields[2:], ""), ",")
		var items []int
		for _, f := range item_fields {
			i, _ := strconv.Atoi(f)
			items = append(items, i)
		}

		monkey := NewMonkey(operation, test)
		monkey.Items = items

		pack.Monkeys = append(pack.Monkeys, monkey)
	}

	return pack
}

func main() {
	pack := ReadInput(os.Args[1])
	for i := 0; i < 20; i += 1 {
		pack.PlayRound()
	}
	fmt.Printf("Solution 1: %d\n", pack.MostActive())

	pack = ReadInput(os.Args[1])
	pack.DecreaseWorry = false
	for i := 0; i < 10000; i += 1 {
		pack.PlayRound()
	}
	fmt.Printf("Solution 2: %d\n", pack.MostActive())
}
