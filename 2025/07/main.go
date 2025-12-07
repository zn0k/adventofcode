package main

import (
	"bufio"
	"fmt"
	"os"
)

// read in the source file using the above helpers
func readInput(fname string) []string {
	file, _ := os.Open(fname)

	defer file.Close()

	var lines []string

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	return lines
}

func main() {
	grid := readInput("input.txt")

	splits := 0
	realities := make([]int64, len(grid[0]))
	for x := 0; x < len(grid[0]); x++ {
		if grid[0][x] == 'S' {
			realities[x] = 1
		}
	}

	for y := 1; y < len(grid); y++ {
		for x := 0; x < len(grid[0]); x++ {
			if grid[y][x] == '^' {
				if realities[x] > 0 {
					splits += 1
					realities[x-1] += realities[x]
					realities[x+1] += realities[x]
					realities[x] = 0
				}
			}
		}
	}
	var sum int64 = 0
	for i := 0; i < len(realities); i++ {
		sum += realities[i]
	}

	fmt.Printf("Solution 1: %d\nSolution 2: %d\n", splits, sum)
}
