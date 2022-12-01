package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
)

// parse input file into a list of lists of ints, each list representing the items for an elf
func ReadInput(path string) [][]int {
	f, err := os.Open(path)
	if err != nil {
		panic(fmt.Sprintf("unable to open %s for reading", path))
	}
	defer f.Close()

	var elves [][]int
	// the current elf
	elf := make([]int, 0)

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		// read next token, default tokenizer returns lines
		line := scanner.Text()
		// if the line is empty, the current elf is done
		if len(line) == 0 {
			// add it to the list of elves
			elves = append(elves, elf)
			// reset current elf
			elf = make([]int, 0)
		} else {
			// parse the current line into an int and add it to the current elf
			i, err := strconv.Atoi(line)
			if err != nil {
				panic(fmt.Sprintf("unable to convert '%s' into an integer", line))
			}
			elf = append(elf, i)
		}
	}

	return elves
}

// does go have a built in sum functin? like hell it does
// we're real programmers and know how to loop
func Sum(items []int) int {
	sum := 0
	for _, item := range items {
		sum += item
	}
	return sum
}

func main() {
	elves := ReadInput(os.Args[1])

	// sum up the elves
	var sums []int
	for _, elf := range elves {
		sums = append(sums, Sum(elf))
	}

	// does go have a max function? ha, you're kidding, right?
	max := 0
	for _, sum := range sums {
		if sum > max {
			max = sum
		}
	}

	fmt.Printf("Solution 1: %d\n", max)

	// alright, then, for part 2 we'll sort properly
	sort.Ints(sums)
	// and sum the biggest three items by taking a slice
	fmt.Printf("Solution 2: %d\n", Sum(sums[len(sums)-3:]))
}
