package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"slices"
)

// naive function to handle errors by panicking
func check(e error) {
	if e != nil {
		panic(e)
	}
}

// read lines in a file into an array of strings
func readLines(f string) ([]string, error) {
	file, err := os.Open(f)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines, scanner.Err()
}

// convert a string of a number to a list of digits as integers
func stringToDigits(s string) ([]int, error) {
	// allocate the slice
	digits := make([]int, 0, len(s))

	for _, r := range s {
		// throw an error if the rune isn't between '0' and '9'
		if r < '0' || r > '9' {
			return nil, fmt.Errorf("invalid digit: %c", r)
		}
		// cast rune to integer
		digits = append(digits, int(r-'0'))
	}
	return digits, nil
}

// convert a list of integer digits to a number
func digitsToInt64(digits []int) int64 {
	var num float64 = 0

	l := len(digits)
	for i := 0; i < l; i++ {
		// multiply digit with appropriate power of 10
		// adding up as we go
		num += float64(digits[i]) * math.Pow10(l-i-1)
	}
	return int64(num)
}

// function to find joltage for a given bank of batteries
// keep finding the largest digits available in a bank while
// leaving enough digits to fill the size requirements
func findJoltage(bank []int, size int) int64 {
	// allocate memory for the digits
	joltage := make([]int, 0, size)
	// loop through the digits
	for i := size - 1; i >= 0; i-- {
		// candidate digits are from the left, but leaving
		// enough digits to fill all slots required for the size
		l := len(bank)
		candidates := bank[:l-i]
		// find the largest digit from the candidates
		largest := slices.Max(candidates)
		// choose it
		joltage = append(joltage, largest)
		// and shrink the available digits for the next iteration
		index := slices.Index(candidates, largest)
		bank = bank[index+1:]
	}
	return digitsToInt64(joltage)
}

func main() {
	// read the lines in the file
	lines, err := readLines("input.txt")
	check(err)

	var solution1 int64 = 0
	var solution2 int64 = 0
	// loop through the battery banks
	for _, line := range lines {
		// convert the string to digits
		digits, err := stringToDigits(line)
		check(err)
		// find the joltages given the two size requirements
		solution1 += findJoltage(digits, 2)
		solution2 += findJoltage(digits, 12)
	}
	fmt.Printf("Solution 1: %d\nSolution 2: %d\n", solution1, solution2)
}
