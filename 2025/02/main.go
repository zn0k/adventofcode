package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

// naive function to handle errors
// by panicking
func check(e error) {
	if e != nil {
		panic(e)
	}
}

// decide if a number is invalid for part 1
func part1(s string) bool {
	// find the half way mark of the string
	half := len(s) / 2
	// repeat it twice
	repeated := strings.Repeat(s[:half], 2)
	// is it the original string
	if repeated == s {
		return true
	}
	return false
}

// decide if a number is invalid for part 2
func part2(s string) bool {
	// find the half way mark of the string
	half := len(s) / 2
	// move up from one character to half of the string
	for i := 1; i <= half; i++ {
		// get the substring up to that character
		sub := s[:i]
		// does it evenly fit into the length of the original string
		if len(s)%len(sub) == 0 {
			// repeat it as many times as needed to make it fit
			repeated := strings.Repeat(sub, len(s)/len(sub))
			// are they the same
			if repeated == s {
				return true
			}
		}
	}
	return false
}

func main() {
	// read the entire file into a string
	input, err := os.ReadFile("input.txt")
	check(err)
	// get the ID ranges by splitting on commas
	ranges := strings.Split(string(input), ",")
	solution1 := 0
	solution2 := 0
	// loop through the ID ranges
	for i := 0; i < len(ranges); i++ {
		// get the beginning and end number
		vals := strings.Split(ranges[i], "-")
		// they're strings, convert to integers
		start, err := strconv.Atoi(vals[0])
		check(err)
		end, err := strconv.Atoi(vals[1])
		check(err)
		// move through the range, including the end number
		for j := start; j <= end; j++ {
			// convert the current ID to a string
			val := strconv.Itoa(j)
			// check for parts 1 and 2
			if part1(val) {
				solution1 += j
			}
			if part2(val) {
				solution2 += j
			}

		}
	}
	fmt.Printf("Solution 1: %d\nSolution 2: %d\n", solution1, solution2)
}
