package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Step struct {
	direction string
	distance  int
}

func readLines(path string) ([]Step, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []Step

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		words := strings.Fields(scanner.Text())
		i64, err := strconv.ParseInt(words[1], 10, 32)
		i := int(i64)
		if err != nil {
			continue
		}
		lines = append(lines, Step{words[0], i})
	}
	return lines, scanner.Err()
}

func main() {
	steps, err := readLines(os.Args[1])
	if err != nil {
		panic(err)
	}

	horizontal, depth := 0, 0
	for _, step := range steps {
		switch step.direction {
		case "forward":
			horizontal += step.distance
		case "up":
			depth -= step.distance
		case "down":
			depth += step.distance
		}
	}
	fmt.Printf("Solution 1: %d\n", horizontal*depth)

	horizontal = 0
	depth = 0
	aim := 0

	for _, step := range steps {
		switch step.direction {
		case "forward":
			horizontal += step.distance
			depth += aim * step.distance
		case "up":
			aim -= step.distance
		case "down":
			aim += step.distance
		}
	}
	fmt.Printf("Solution 2: %d\n", horizontal*depth)
}
