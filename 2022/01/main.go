package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
)

// does go have a built in sum functin? like hell it does
// we're real programmers and know how to loop
func Sum(items []int) int {
	sum := 0
	for _, item := range items {
		sum += item
	}
	return sum
}

// parse input file into the summed calories for each elf
func ReadInput(path string) []int {
	f, err := os.Open(path)
	if err != nil {
		panic(fmt.Sprintf("unable to open %s for reading", path))
	}
	defer f.Close()

	var elves []int
	// the current elf
	elf := 0

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		// read next token, default tokenizer returns lines
		line := scanner.Text()
		// if the line is empty, the current elf is done
		if len(line) == 0 {
			// sum it and add it to the list of elves
			elves = append(elves, elf)
			// reset current elf
			elf = 0
		} else {
			// parse the current line into an int and add it to the current elf
			i, err := strconv.Atoi(line)
			if err != nil {
				panic(fmt.Sprintf("unable to convert '%s' into an integer", line))
			}
			elf += i
		}
	}

	return elves
}

func main() {
	elves := ReadInput(os.Args[1])

	// sort the calories
	sort.Ints(elves)

	fmt.Printf("Solution 1: %d\n", elves[len(elves)-1])
	// and sum the biggest three items by taking a slice
	fmt.Printf("Solution 2: %d\n", Sum(elves[len(elves)-3:]))
}
