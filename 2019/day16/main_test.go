package main

import (
	"testing"
)

func TestPatternGeneration(t *testing.T) {
	tests := []struct {
		length   int
		element  int
		expected []int
	}{
		{
			length: 8, element: 0, expected: []int{1, 0, -1, 0, 1, 0, -1, 0},
		},
		{
			length: 8, element: 1, expected: []int{0, 1, 1, 0, 0, -1, -1, 0},
		},
		{
			length: 8, element: 2, expected: []int{0, 0, 1, 1, 1, 0, 0, 0},
		},
	}

	for _, tt := range tests {
		result := GeneratePattern(tt.length, tt.element)
		compareIntLists(t, result, tt.expected)
	}
}

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
		patterns := GeneratePatterns(len(signal))
		result := Process(signal, patterns, tt.iterations)
		compareIntLists(t, result, tt.out)
	}
}
