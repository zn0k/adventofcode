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

type IntCodeMemory map[int64]int64

type IntCodeComputer struct {
	memory              IntCodeMemory
	instructionPointer  int64
	relativeBasePointer int64
}

type OpCode interface {
	Code() int64
	Execute(ic *IntCodeComputer)
}

type genericOpCode struct {
	code       int64
	params     int64
	paramModes []int64
}

type ADD genericOpCode
type MUL genericOpCode
type HLT genericOpCode

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
	op := ic.parseOpCode()
	for op.Code() != 99 {
		op.Execute(ic)
		op = ic.parseOpCode()
	}
}

func (ic *IntCodeComputer) parseOpCode() OpCode {
	val := ic.Read(ic.instructionPointer)
	opModeA := val / 10000
	opModeB := val / 1000
	opModeC := val / 100
	opCode := val - (10000 * opModeA) - (1000 * opModeB) - (100 * opModeC)
	switch opCode {
	case 1:
		return &ADD{
			code:       1,
			params:     3,
			paramModes: []int64{opModeC, opModeB, opModeA},
		}
	case 2:
		return &MUL{
			code:       2,
			params:     3,
			paramModes: []int64{opModeC, opModeB, opModeA},
		}
	case 99:
		return &HLT{
			code:       99,
			params:     0,
			paramModes: []int64{},
		}
	default:
		panic(fmt.Sprintf("Unknown op code %d with parameter modes (%d, %d, %d)", opCode, opModeC, opModeB, opModeA))
	}
}

func (ic *IntCodeComputer) readParameter(addr int64, mode int64) int64 {
	switch mode {
	case 0:
		return ic.Read(addr)
	case 1:
		return addr
	case 2:
		return ic.Read(ic.relativeBasePointer + addr)
	default:
		panic(fmt.Sprintf("Unknown parameter mode %d", mode))
	}
}

func (op *ADD) Code() int64 { return op.code }
func (op *ADD) Execute(ic *IntCodeComputer) {
	left := ic.readParameter(ic.instructionPointer+1, op.paramModes[0])
	right := ic.readParameter(ic.instructionPointer+2, op.paramModes[1])
	ic.Write(ic.readParameter(ic.instructionPointer+3, op.paramModes[2]), left+right)
	ic.instructionPointer = ic.instructionPointer + 4
}

func (op *MUL) Code() int64 { return op.code }
func (op *MUL) Execute(ic *IntCodeComputer) {
	left := ic.readParameter(ic.instructionPointer+1, op.paramModes[0])
	right := ic.readParameter(ic.instructionPointer+2, op.paramModes[1])
	ic.Write(ic.readParameter(ic.instructionPointer+3, op.paramModes[2]), left*right)
	ic.instructionPointer = ic.instructionPointer + 4
}

func (op *HLT) Code() int64                 { return op.code }
func (op *HLT) Execute(ic *IntCodeComputer) {}
