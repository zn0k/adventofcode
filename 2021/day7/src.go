package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

func readLines(path string) ([]int, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var positions []int

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		fields := strings.Split(line, ",")
		for _, field := range fields {
			asInt, err := strconv.ParseInt(field, 10, 32)
			if nil != err {
				return nil, err
			}
			positions = append(positions, int(asInt))
		}
	}

	return positions, scanner.Err()
}

func minMax(xs []int) (int, int) {
	max, min := xs[0], xs[0]
	for _, x := range xs {
		if max < x {
			max = x
		}
		if min > x {
			min = x
		}
	}
	return min, max
}

func main() {
	positions, err := readLines(os.Args[1])
	if err != nil {
		panic(err)
	}

	minPos, maxPos := minMax(positions)

	var solutions1, solutions2 []int

	for to := minPos; to <= maxPos; to++ {
		cost1, cost2 := 0, 0
		for _, pos := range positions {
			cost1 += int(math.Abs(float64(pos - to)))
			for i := 1; i <= int(math.Abs(float64(pos-to))); i++ {
				cost2 += i
			}
		}
		solutions1 = append(solutions1, cost1)
		solutions2 = append(solutions2, cost2)
	}

	solution1, _ := minMax(solutions1)
	solution2, _ := minMax(solutions2)

	fmt.Printf("Solution 1: %d\n", solution1)
	fmt.Printf("Solution 2: %d\n", solution2)
}
