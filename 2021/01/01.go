package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func readLines(path string) ([]int64, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []int64

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		s := scanner.Text()
		i, err := strconv.ParseInt(s, 10, 64)
		if err != nil {
			continue
		}
		lines = append(lines, i)
	}
	return lines, scanner.Err()
}

func countIncreases(data []int64) int64 {
	var previous, increases int64 = data[0], 0

	for _, val := range data {
		if val > previous {
			increases += 1
		}
		previous = val
	}

	return increases
}

func getWindows(data []int64) []int64 {
	var windows []int64

	for i := 0; i < len(data)-2; i++ {
		sum := data[i] + data[i+1] + data[i+2]
		windows = append(windows, sum)
	}
	return windows
}

func main() {
	file := "input.txt"
	lines, err := readLines(file)
	if err != nil {
		log.Fatalf("Error reading file %s: %v", file, err)
	}

	fmt.Printf("Solution 1: %d\n", countIncreases(lines))
	fmt.Printf("Solution 2: %d\n", countIncreases(getWindows(lines)))
}
