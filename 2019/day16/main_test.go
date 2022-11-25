package main

import (
	"strings"
	"testing"
)

func compareIntLists(t *testing.T, a, b []int) bool {
	if len(a) != len(b) {
		t.Errorf("returned list does not have length %d, got %d", len(b), len(a))
		return false
	}
	for i := 0; i < len(a); i++ {
		if a[i] != b[i] {
			t.Errorf("element %d is different, expected %d and got %d", i, b[i], a[i])
			return false
		}
	}
	return true
}

func TestStringToSlice(t *testing.T) {
	tests := []struct {
		in  string
		out []int
	}{
		{
			in: "12345", out: []int{1, 2, 3, 4, 5},
		},
		{
			in: "9876543210", out: []int{9, 8, 7, 6, 5, 4, 3, 2, 1, 0},
		},
	}

	for _, tt := range tests {
		result := StringToSlice(tt.in)
		compareIntLists(t, result, tt.out)
	}
}

func TestProcess(t *testing.T) {
	tests := []struct {
		in         string
		iterations int
		out        []int
	}{
		{
			in: "12345678", iterations: 1, out: []int{4, 8, 2, 2, 6, 1, 5, 8},
		},
		{
			in: "12345678", iterations: 4, out: []int{0, 1, 0, 2, 9, 4, 9, 8},
		},
		{
			in: "80871224585914546619083218645595", iterations: 100, out: []int{2, 4, 1, 7, 6, 1, 7, 6},
		},
		{
			in: "19617804207202209144916044189917", iterations: 100, out: []int{7, 3, 7, 4, 5, 4, 1, 8},
		},
		{
			in: "69317163492948606335995924319873", iterations: 100, out: []int{5, 2, 4, 3, 2, 1, 3, 3},
		},
	}

	for _, tt := range tests {
		signal := StringToSlice(tt.in)
		result := Process(signal, tt.iterations)
		compareIntLists(t, result, tt.out)
	}
}

func TestProcess2(t *testing.T) {
	tests := []struct {
		in         string
		iterations int
		out        []int
	}{
		{
			in: "03036732577212944063491565474664", iterations: 100, out: []int{8, 4, 4, 6, 2, 0, 2, 6},
		},
		{
			in: "02935109699940807407585447034323", iterations: 100, out: []int{7, 8, 7, 2, 5, 2, 7, 0},
		},
		{
			in: "03081770884921959731165446850517", iterations: 100, out: []int{5, 3, 5, 5, 3, 7, 3, 1},
		},
	}

	for _, tt := range tests {
		input := strings.Repeat(tt.in, 10000)
		signal := StringToSlice(input)
		result := Process2(signal, tt.iterations)
		compareIntLists(t, result, tt.out)
	}
}
