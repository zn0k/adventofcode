package intcode

import (
	"io"
	"strconv"
	"strings"
	"testing"
)

func programFromInts(in []int64) io.Reader {
	ss := []string{}
	for _, t := range in {
		ss = append(ss, strconv.FormatInt(t, 10))
	}
	return strings.NewReader(strings.Join(ss, ","))
}

func TestIntCodeRead(t *testing.T) {
	test := map[int64]int64{
		1: 1,
		2: 2,
	}
	in := make(chan int64, 1)
	out := make(chan int64, 1)
	ic := New(in, out)
	for k, v := range test {
		ic.memory[k] = v
	}

	for k, v := range test {
		if ic.Read(k) != v {
			t.Errorf("Memory value at address %d is not %d, got %d", k, v, ic.Read(k))
		}
	}
}

func TestIntCodeWrite(t *testing.T) {
	test := map[int64]int64{
		1: 1,
		2: 2,
	}

	in := make(chan int64, 2)
	out := make(chan int64, 2)
	ic := New(in, out)
	for k, v := range test {
		ic.Write(k, v)
		if ic.memory[k] != v {
			t.Errorf("Memory value at address %d is not %d, got %d", k, v, ic.memory[k])
		}
	}
}

func TestIntCodeLoader(t *testing.T) {
	test := []int64{1, 0, 0, 3, 99}
	in := make(chan int64, 2)
	out := make(chan int64, 2)
	ic := New(in, out)
	ic.Load(programFromInts(test))
	for i, tt := range test {
		if ic.Read(int64(i)) != tt {
			t.Errorf("Memory value at address %d is not %d, got %d", i, tt, ic.Read(int64(i)))
		}
	}
}

func TestIntCodeDay2(t *testing.T) {
	tests := []struct {
		input         []int64
		addr          int64
		expectedValue int64
	}{
		{input: []int64{1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50}, addr: 0, expectedValue: 3500},
		{input: []int64{1, 0, 0, 0, 99}, addr: 0, expectedValue: 2},
		{input: []int64{2, 3, 0, 3, 99}, addr: 3, expectedValue: 6},
		{input: []int64{2, 4, 4, 5, 99, 0}, addr: 5, expectedValue: 9801},
		{input: []int64{1, 1, 1, 4, 99, 5, 6, 0, 99}, addr: 0, expectedValue: 30},
	}

	for _, tt := range tests {
		in := make(chan int64, 2)
		out := make(chan int64, 2)
		ic := New(in, out)
		ic.Load(programFromInts(tt.input))
		ic.Run()

		if ic.Read(tt.addr) != tt.expectedValue {
			t.Errorf("Memory value at address %d is not %d, got %d", tt.addr, tt.expectedValue, ic.Read(tt.addr))
		}
	}
}

func TestIntCodeInput(t *testing.T) {
	test := []int64{3, 0, 99}
	in := make(chan int64, 2)
	out := make(chan int64, 2)
	ic := New(in, out)
	ic.Load(programFromInts(test))
	in <- 100
	ic.Run()

	if ic.Read(0) != 100 {
		t.Errorf("Memory value at address %d is not %d, got %d", 0, 100, ic.Read(0))
	}
}

func TestIntCodeOutput(t *testing.T) {
	test := []int64{4, 3, 99, 100}
	in := make(chan int64, 2)
	out := make(chan int64, 2)
	ic := New(in, out)
	ic.Load(programFromInts(test))
	ic.Run()
	result := <-out

	if result != 100 {
		t.Errorf("Returned value is not %d, got %d", 100, result)
	}
}

func TestIntCodeDay5(t *testing.T) {
	tests := []struct {
		input         []int64
		addr          int64
		expectedValue int64
	}{
		{input: []int64{1002, 4, 3, 4, 33}, addr: 4, expectedValue: 99},
	}

	for _, tt := range tests {
		in := make(chan int64)
		out := make(chan int64)
		ic := New(in, out)
		ic.Load(programFromInts(tt.input))
		ic.Run()

		if ic.Read(tt.addr) != tt.expectedValue {
			t.Errorf("Memory value at address %d is not %d, got %d", tt.addr, tt.expectedValue, ic.Read(tt.addr))
		}
	}
}

func TestIntCodeDay5Part2(t *testing.T) {
	tests := []struct {
		program        []int64
		input          int64
		expectedOutput int64
	}{
		{program: []int64{3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8}, input: 8, expectedOutput: 1},
		{program: []int64{3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8}, input: 7, expectedOutput: 0},
		{program: []int64{3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8}, input: 7, expectedOutput: 1},
		{program: []int64{3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8}, input: 9, expectedOutput: 0},
		{program: []int64{3, 3, 1108, -1, 8, 3, 4, 3, 99}, input: 8, expectedOutput: 1},
		{program: []int64{3, 3, 1108, -1, 8, 3, 4, 3, 99}, input: 7, expectedOutput: 0},
		{program: []int64{3, 3, 1107, -1, 8, 3, 4, 3, 99}, input: 7, expectedOutput: 1},
		{program: []int64{3, 3, 1107, -1, 8, 3, 4, 3, 99}, input: 9, expectedOutput: 0},
		{program: []int64{3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9}, input: 0, expectedOutput: 0},
		{program: []int64{3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9}, input: 10, expectedOutput: 1},
		{program: []int64{3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
			1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
			999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99}, input: 7, expectedOutput: 999},
		{program: []int64{3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
			1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
			999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99}, input: 8, expectedOutput: 1000},
		{program: []int64{3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
			1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
			999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99}, input: 9, expectedOutput: 1001},
	}

	for _, tt := range tests {
		in := make(chan int64, 2)
		out := make(chan int64, 2)
		ic := New(in, out)
		ic.Load(programFromInts(tt.program))
		in <- tt.input
		ic.Run()
		result := <-out

		if result != tt.expectedOutput {
			t.Errorf("Output is not %d, got %d", tt.expectedOutput, result)
		}
	}
}

func TestIntCodeDay9(t *testing.T) {
	test := []int64{104, 1125899906842624, 99}
	in := make(chan int64, 2)
	out := make(chan int64, 2)
	ic := New(in, out)
	ic.Load(programFromInts(test))
	ic.Run()
	result := <-out

	if result != 1125899906842624 {
		t.Errorf("Returned value is not %d, got %d", 1125899906842624, result)
	}

	test = []int64{1102, 34915192, 34915192, 7, 4, 7, 99, 0}
	in = make(chan int64, 2)
	out = make(chan int64, 2)
	ic = New(in, out)
	ic.Load(programFromInts(test))
	ic.Run()
	result = <-out

	if len(strconv.FormatInt(result, 10)) != 16 {
		t.Errorf("Returned value does not have 16 digits, got %d", result)
	}

	test = []int64{109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99}
	in = make(chan int64, 2)
	out = make(chan int64, 2)
	ic = New(in, out)
	ic.Load(programFromInts(test))
	go ic.Run()
	var quine []int64
	for r := range out {
		quine = append(quine, r)
	}
	for i, v := range test {
		if quine[i] != v {
			t.Errorf("Returned quine value at index %d is not %d, got %d", i, test[i], quine[i])
		}
	}
}
