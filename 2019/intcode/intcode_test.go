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
	ic := New()
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

	ic := New()
	for k, v := range test {
		ic.Write(k, v)
		if ic.memory[k] != v {
			t.Errorf("Memory value at address %d is not %d, got %d", k, v, ic.memory[k])
		}
	}
}

func TestIntCodeLoader(t *testing.T) {
	test := []int64{1, 0, 0, 3, 99}
	ic := New()
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
		ic := New()
		ic.Load(programFromInts(tt.input))
		ic.Run()

		if ic.Read(tt.addr) != tt.expectedValue {
			t.Errorf("Memory value at address %d is not %d, got %d", tt.addr, tt.expectedValue, ic.Read(tt.addr))
		}
	}
}
