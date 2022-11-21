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
	HLT int64 = 99
)

type IntCodeMemory map[int64]int64

type IntCodeComputer struct {
	memory              IntCodeMemory
	instructionPointer  int64
	relativeBasePointer int64
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

func New() *IntCodeComputer {
	ic := &IntCodeComputer{instructionPointer: 0, relativeBasePointer: 0}
	ic.memory = make(IntCodeMemory)
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
	for code != 99 {
		op.Execute(ic)
		op, code = ic.parseOpCode()
	}
}

func (ic *IntCodeComputer) parseOpCode() (OpCode, int64) {
	val := ic.Read(ic.instructionPointer)
	opModeA := val / 10000
	opModeB := val / 1000
	opModeC := val / 100
	opCode := val - (10000 * opModeA) - (1000 * opModeB) - (100 * opModeC)
	switch opCode {
	case 1:
		return &Add{
			code:       1,
			params:     3,
			paramModes: []int64{opModeC, opModeB, opModeA},
		}, ADD
	case 2:
		return &Mul{
			code:       2,
			params:     3,
			paramModes: []int64{opModeC, opModeB, opModeA},
		}, MUL
	case 99:
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

func (op *Add) Code() int64 { return op.code }
func (op *Add) Execute(ic *IntCodeComputer) {
	left := ic.readParameter(ic.instructionPointer+1, op.paramModes[0])
	right := ic.readParameter(ic.instructionPointer+2, op.paramModes[1])
	writeAddr := ic.Read(ic.instructionPointer + 3)
	ic.Write(writeAddr, left+right)
	ic.instructionPointer = ic.instructionPointer + 4
}

func (op *Mul) Code() int64 { return op.code }
func (op *Mul) Execute(ic *IntCodeComputer) {
	left := ic.readParameter(ic.instructionPointer+1, op.paramModes[0])
	right := ic.readParameter(ic.instructionPointer+2, op.paramModes[1])
	writeAddr := ic.Read(ic.instructionPointer + 3)
	ic.Write(writeAddr, left*right)
	ic.instructionPointer = ic.instructionPointer + 4
}

func (op *Hlt) Code() int64                 { return op.code }
func (op *Hlt) Execute(ic *IntCodeComputer) {}
