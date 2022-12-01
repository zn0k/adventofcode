package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func main() {
	f, err := os.Open(os.Args[1])
	if err != nil {
		panic(fmt.Sprintf("unable to open %s for reading", os.Args[1]))
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)
	var changes []int
	for scanner.Scan() {
		line := scanner.Text()
		num, err := strconv.ParseInt(line, 10, 32)
		if err != nil {
			panic(fmt.Sprintf("unable to convert %q into integer", line))
		}
		changes = append(changes, int(num))
	}

	solution1 := 0
	for _, num := range changes {
		solution1 += num
	}

	sum := 0
	seen := make(map[int]bool)
	var solution2 int
	solution2Found := false
	for !solution2Found {
		for _, num := range changes {
			_, ok := seen[sum]
			if ok && !solution2Found {
				solution2Found = true
				solution2 = sum
				break
			}
			seen[sum] = true
			sum += num
		}
	}
	fmt.Printf("Solution 1: %d\nSolution 2: %d\n", solution1, solution2)
}
