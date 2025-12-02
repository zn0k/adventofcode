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
	// repeat it twice, see if it's the original
	return strings.Repeat(s[:half], len(s)/2) == s
}

// decide if a number is invalid for part 2
func part2(s string) bool {
	// find length of the original string
	n := len(s)
	// and the halfway mark
	half := len(s) / 2
	// move up from one character to half of the string
	for size := 1; size <= half; size++ {
		// if this size doesn't evenly sit, bail
		if n%size != 0 {
			continue
		}
		ok := true
		// go through the remainder of the string, past
		// the first bit we're trying to find repeats for
		for i := size; i < n; i++ {
			// check if the current character matches the
			// relevant spot in the substring we're repeating
			if s[i] != s[i%size] {
				ok = false
				break
			}
		}
		if ok {
			// string is invalid
			return true
		}
	}
	return false
}

func main() {
	// read the entire file into a string
	input, err := os.ReadFile("input.txt")
	check(err)
	// get the ID ranges by splitting on commas
	ranges := strings.Split(strings.TrimSpace(string(input)), ",")
	solution1 := 0
	solution2 := 0
	// loop through the ID ranges
	for _, r := range ranges {
		// get the beginning and end number
		vals := strings.Split(r, "-")
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
