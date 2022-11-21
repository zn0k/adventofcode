package intcode

import (
	"bufio"
	"fmt"
	"io"
	"strconv"
	"strings"
)

const (
	POSITION  int64 = 0
	IMMEDIATE int64 = 1
	RELATIVE  int64 = 2
)

const (
	ADD int64 = 1
	MUL int64 = 2
	PSH int64 = 3
	POP int64 = 4
	JNZ int64 = 5
	JEZ int64 = 6
	CLT int64 = 7
	CMP int64 = 8
	HLT int64 = 99
)

type IntCodeMemory map[int64]int64

type IntCodeComputer struct {
	memory              IntCodeMemory
	instructionPointer  int64
	relativeBasePointer int64
	input               chan int64
	output              chan int64
}

type OpCode interface {
	Execute(ic *IntCodeComputer)
}

type genericOpCode struct {
	code       int64
	params     int64
	paramModes []int64
}

type Add genericOpCode
type Mul genericOpCode
type Hlt genericOpCode
type Psh genericOpCode
type Pop genericOpCode
type Jnz genericOpCode
type Jez genericOpCode
type Clt genericOpCode
type Cmp genericOpCode

func New(in chan int64, out chan int64) *IntCodeComputer {
	ic := &IntCodeComputer{instructionPointer: 0, relativeBasePointer: 0}
	ic.memory = make(IntCodeMemory)
	ic.input = in
	ic.output = out
	return ic
}

func (ic *IntCodeComputer) Load(in io.Reader) {
	scanner := bufio.NewScanner(in)
	buffer := []int64{}
	for scanner.Scan() {
		for _, value := range strings.Split(scanner.Text(), ",") {
			i, ok := strconv.ParseInt(value, 10, 64)
			if ok != nil {
				panic(fmt.Sprintf("Unable to parse '%s' as a base 10 int64", value))
			}
			buffer = append(buffer, i)
		}
	}
	for i, val := range buffer {
		ic.Write(int64(i), val)
	}
}

func (ic *IntCodeComputer) Read(addr int64) int64 {
	return ic.memory[addr]
}

func (ic *IntCodeComputer) Write(addr, val int64) {
	ic.memory[addr] = val
}

func (ic *IntCodeComputer) Run() {
	op, code := ic.parseOpCode()
	for code != HLT {
		op.Execute(ic)
		op, code = ic.parseOpCode()
	}
	// execute the HLT op
	op.Execute(ic)
}

func (ic *IntCodeComputer) parseOpCode() (OpCode, int64) {
	val := ic.Read(ic.instructionPointer)
	opModeA := val / 10000
	val = val - (10000 * opModeA)
	opModeB := val / 1000
	val = val - (1000 * opModeB)
	opModeC := val / 100
	opCode := val - (100 * opModeC)
	switch opCode {
	case ADD:
		return &Add{
			code:       1,
			params:     3,
			paramModes: []int64{opModeC, opModeB, opModeA},
		}, ADD
	case MUL:
		return &Mul{
			code:       2,
			params:     3,
			paramModes: []int64{opModeC, opModeB, opModeA},
		}, MUL
	case PSH:
		return &Psh{
			code:       3,
			params:     1,
			paramModes: []int64{opModeC},
		}, PSH
	case POP:
		return &Pop{
			code:       4,
			params:     1,
			paramModes: []int64{opModeC},
		}, POP
	case JNZ:
		return &Jnz{
			code:       5,
			params:     2,
			paramModes: []int64{opModeC, opModeB},
		}, JNZ
	case JEZ:
		return &Jez{
			code:       6,
			params:     2,
			paramModes: []int64{opModeC, opModeB},
		}, JEZ
	case CLT:
		return &Clt{
			code:       7,
			params:     3,
			paramModes: []int64{opModeC, opModeB, opModeA},
		}, CLT
	case CMP:
		return &Cmp{
			code:       8,
			params:     3,
			paramModes: []int64{opModeC, opModeB, opModeA},
		}, CMP
	case HLT:
		return &Hlt{
			code:       99,
			params:     0,
			paramModes: []int64{},
		}, HLT
	default:
		panic(fmt.Sprintf("Unknown op code %d with parameter modes (%d, %d, %d)", opCode, opModeC, opModeB, opModeA))
	}
}

func (ic *IntCodeComputer) readParameter(addr int64, mode int64) int64 {
	switch mode {
	case POSITION:
		return ic.Read(ic.Read(addr))
	case IMMEDIATE:
		return ic.Read(addr)
	case RELATIVE:
		return ic.Read(ic.relativeBasePointer + addr)
	default:
		panic(fmt.Sprintf("Unknown parameter mode %d", mode))
	}
}

func (op *Add) Execute(ic *IntCodeComputer) {
	left := ic.readParameter(ic.instructionPointer+1, op.paramModes[0])
	right := ic.readParameter(ic.instructionPointer+2, op.paramModes[1])
	writeAddr := ic.Read(ic.instructionPointer + 3)
	ic.Write(writeAddr, left+right)
	ic.instructionPointer = ic.instructionPointer + 4
}

func (op *Mul) Execute(ic *IntCodeComputer) {
	left := ic.readParameter(ic.instructionPointer+1, op.paramModes[0])
	right := ic.readParameter(ic.instructionPointer+2, op.paramModes[1])
	writeAddr := ic.Read(ic.instructionPointer + 3)
	ic.Write(writeAddr, left*right)
	ic.instructionPointer = ic.instructionPointer + 4
}

func (op *Hlt) Execute(ic *IntCodeComputer) {
	close(ic.output)
}

func (op *Psh) Execute(ic *IntCodeComputer) {
	writeAddr := ic.Read(ic.instructionPointer + 1)
	val := <-ic.input
	ic.Write(writeAddr, val)
	ic.instructionPointer = ic.instructionPointer + 2
}

func (op *Pop) Execute(ic *IntCodeComputer) {
	val := ic.readParameter(ic.instructionPointer+1, op.paramModes[0])
	ic.output <- val
	ic.instructionPointer = ic.instructionPointer + 2
}

func (op *Jnz) Execute(ic *IntCodeComputer) {
	val := ic.readParameter(ic.instructionPointer+1, op.paramModes[0])
	if val != 0 {
		ic.instructionPointer = ic.readParameter(ic.instructionPointer+2, op.paramModes[1])
	} else {
		ic.instructionPointer = ic.instructionPointer + 3
	}
}

func (op *Jez) Execute(ic *IntCodeComputer) {
	val := ic.readParameter(ic.instructionPointer+1, op.paramModes[0])
	if val == 0 {
		ic.instructionPointer = ic.readParameter(ic.instructionPointer+2, op.paramModes[1])
	} else {
		ic.instructionPointer = ic.instructionPointer + 3
	}
}

func (op *Clt) Execute(ic *IntCodeComputer) {
	left := ic.readParameter(ic.instructionPointer+1, op.paramModes[0])
	right := ic.readParameter(ic.instructionPointer+2, op.paramModes[1])
	writeAddr := ic.Read(ic.instructionPointer + 3)
	if left < right {
		ic.Write(writeAddr, 1)
	} else {
		ic.Write(writeAddr, 0)
	}
	ic.instructionPointer = ic.instructionPointer + 4
}

func (op *Cmp) Execute(ic *IntCodeComputer) {
	left := ic.readParameter(ic.instructionPointer+1, op.paramModes[0])
	right := ic.readParameter(ic.instructionPointer+2, op.paramModes[1])
	writeAddr := ic.Read(ic.instructionPointer + 3)
	if left == right {
		ic.Write(writeAddr, 1)
	} else {
		ic.Write(writeAddr, 0)
	}
	ic.instructionPointer = ic.instructionPointer + 4
}
