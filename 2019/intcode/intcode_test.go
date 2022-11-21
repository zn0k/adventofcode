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

func TestIntCodeADD(t *testing.T) {
	test := []int64{1, 1, 1, 5, 99, 0}
	ic := New()
	ic.Load(programFromInts(test))
	ic.Run()
	if ic.Read(5) != 2 {
		t.Errorf("Memory value at address 5 is not 2, got %d", ic.Read(5))
	}
}

func TestIntCodeMUL(t *testing.T) {
	test := []int64{2, 2, 3, 5, 99, 0}
	ic := New()
	ic.Load(programFromInts(test))
	ic.Run()
	if ic.Read(5) != 6 {
		t.Errorf("Memory value at address 5 is not 6, got %d", ic.Read(5))
	}
}
