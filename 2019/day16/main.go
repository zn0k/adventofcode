package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"strconv"
)

func GeneratePattern(length int, element int) []int {
	base := []int{0, 1, 0, -1}
	result := make([]int, length+1)
	for i := 0; i < len(result); i++ {
		result[i] = base[(i/(element+1))%len(base)]
	}
	return result[1:]
}

func GeneratePatterns(length int) [][]int {
	var result [][]int
	for i := 0; i < length; i++ {
		row := GeneratePattern(length, i)
		result = append(result, row)
	}
	return result
}

func StringToSlice(s string) []int {
	result := make([]int, len(s))
	for i, r := range s {
		num, err := strconv.ParseInt(string(r), 10, 32)
		if err != nil {
			panic("unable to parse digit as integer")
		}
		result[i] = int(num)
	}
	return result
}

func Process(signal []int, patterns [][]int, iterations int) []int {
	result := make([]int, len(signal))

	for iteration := 0; iteration < iterations; iteration++ {
		for digit := 0; digit < len(signal); digit++ {
			sum := 0
			for i := 0; i < len(signal); i++ {
				sum += signal[i] * patterns[digit][i]
			}
			result[digit] = int(math.Abs(float64(sum))) % 10
		}
		signal = result
	}
	if len(result) > 8 {
		return result[0:8]
	} else {
		return result
	}
}

func Stringify(digits []int) string {
	result := ""
	for _, d := range digits {
		result += strconv.FormatInt(int64(d), 10)
	}
	return result
}

func main() {
	buf, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic("unable to open input.txt")
	}
	signal := StringToSlice(string(buf))
	patterns := GeneratePatterns(len(signal))

	result := Process(signal, patterns, 100)
	fmt.Printf("Solution 1: %s\n", Stringify(result))
}
