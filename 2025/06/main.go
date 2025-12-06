package main

import (
	"bufio"
	"fmt"
	"math/big"
	"os"
	"strconv"
	"strings"
)

// extract the column ranges from a string like
// *  +  *  *  +
// each column starts with a non-space characer and ends at the next one
func extractRanges(in string, end_index int) [][]int {
	indices := make([]int, 0, len(in)/2)
	for i, r := range in {
		if r != ' ' {
			indices = append(indices, i)
		}
	}

	ranges := make([][]int, 0, len(indices)+1)
	for i, idx := range indices {
		if i == len(indices)-1 {
			ranges = append(ranges, []int{idx, end_index})
		} else {
			ranges = append(ranges, []int{idx, indices[i+1]})
		}
	}
	return ranges
}

// generic function to transpose a list of lists
func transpose[T any](matrix [][]T) [][]T {
	if len(matrix) == 0 {
		return [][]T{}
	}

	rows := len(matrix)
	cols := len(matrix[0])

	transposed := make([][]T, cols)
	for i := range transposed {
		transposed[i] = make([]T, rows)
	}

	for i := 0; i < rows; i++ {
		for j := 0; j < cols; j++ {
			transposed[j][i] = matrix[i][j]
		}
	}
	return transposed
}

// extract the numbers for part 1, as big.Ints
func extractNumbersPart1(homework []string, ranges [][]int) [][]*big.Int {
	extracted := make([][]*big.Int, len(homework))
	for i := range extracted {
		extracted[i] = make([]*big.Int, len(ranges))
	}

	// loop through the matrix
	for i, s := range homework {
		for j, r := range ranges {
			// remove spaces
			sub := strings.TrimSpace(s[r[0] : r[1]-1])
			// cast to an integer
			num, _ := strconv.Atoi(sub)
			// cast to a big.Int
			extracted[i][j] = big.NewInt(int64(num))
		}
	}

	// and tranpose because we're looking at columns
	return transpose((extracted))
}

// extract the numbers for part 2
func extractNumbersPart2(homework []string, ranges [][]int) [][]*big.Int {
	// extract as strings for starters
	extracted := make([][]string, len(homework))
	for i := range extracted {
		extracted[i] = make([]string, len(ranges))
	}

	for i, s := range homework {
		for j, r := range ranges {
			extracted[i][j] = s[r[0] : r[1]-1]
		}
	}

	// extract the actual numbers
	result := make([][]*big.Int, len(ranges))
	for i, problem := range transpose(extracted) {
		// first, case each sub-string to a list of runes
		runes := make([][]rune, len(problem))
		for j := range problem {
			runes[j] = []rune(problem[j])
		}
		// transpose the runes to look at columns
		runes = transpose(runes)
		// and then extract the big.Ints as above
		nums := make([]*big.Int, len(runes))
		for j := range runes {
			str := strings.TrimSpace(string(runes[j]))
			num, _ := strconv.Atoi(str)
			nums[j] = big.NewInt(int64(num))
		}
		result[i] = nums
	}

	return result
}

// extract the actual operators as a list of runes
func extractOperators(ops_line string, ranges [][]int) []rune {
	operators := make([]rune, len(ranges))
	for i, r := range ranges {
		operators[i] = rune(ops_line[r[0]])
	}

	return operators
}

// read in the source file using the above helpers
func readInput(fname string) ([][]*big.Int, [][]*big.Int, []rune) {
	file, _ := os.Open(fname)

	defer file.Close()

	var lines []string

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	ranges := extractRanges(lines[len(lines)-1], len(lines[0])+1)
	part1 := extractNumbersPart1(lines[:len(lines)-1], ranges)
	part2 := extractNumbersPart2(lines[:len(lines)-1], ranges)
	operators := extractOperators(lines[len(lines)-1], ranges)

	return part1, part2, operators
}

// reduce a list of big.Ints via addition
func reduceAdd(nums []*big.Int) *big.Int {
	result := big.NewInt(0)
	for _, num := range nums {
		result.Add(result, num)
	}
	return result
}

// reduce them via multiplications
func reduceMul(nums []*big.Int) *big.Int {
	result := big.NewInt(1)
	for _, num := range nums {
		result.Mul(result, num)
	}
	return result
}

// and run
func main() {
	// read the input
	part1, part2, operators := readInput("input.txt")
	solution1 := big.NewInt(0)
	solution2 := big.NewInt(0)

	// iterate over each problem
	for i, op := range operators {
		switch op {
		// add or multiply depending on the operator
		case '+':
			solution1.Add(solution1, reduceAdd(part1[i]))
			solution2.Add(solution2, reduceAdd(part2[i]))
		case '*':
			solution1.Add(solution1, reduceMul(part1[i]))
			solution2.Add(solution2, reduceMul(part2[i]))
		}
	}
	fmt.Printf("Solution 1: %v\nSolution 2: %v\n", solution1, solution2)
}
