package main

import (
	"intcode"
	"strings"
	"testing"
)

func TestDay2(t *testing.T) {
	input := "1,9,10,3,2,3,11,0,99,30,40,50"
	ic := intcode.New()
	ic.Load(strings.NewReader(input))
	ic.Run()
	if ic.Read(0) != 3500 {
		t.Errorf("memory value at position 0 is not 3500, got %d", ic.Read(0))
	}
}
