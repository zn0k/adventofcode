package main

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

func TestDay7(t *testing.T) {
	tests := []struct {
		program       string
		sequence      []int64
		expectedValue int64
	}{
		{
			program:       "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0",
			sequence:      []int64{4, 3, 2, 1, 0},
			expectedValue: 43210,
		},
		{
			program:       "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0",
			sequence:      []int64{0, 1, 2, 3, 4},
			expectedValue: 54321,
		},
		{
			program:       "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0",
			sequence:      []int64{1, 0, 4, 3, 2},
			expectedValue: 65210,
		},
	}

	for _, tt := range tests {
		result := runSequence(tt.program, tt.sequence)
		if result != tt.expectedValue {
			t.Errorf("final output is not %d, got %d\n", tt.expectedValue, result)
		}
	}
}
