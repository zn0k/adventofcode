package aoc

import (
	"bufio"
	"os"
	"strconv"
	"strings"

	"gonum.org/v1/gonum/mat"
)

// function to read a given file into a slice of strings
func ReadLines(path string) (lines []string) {
	file, err := os.Open(path)
	if err != nil {
		panic(err)
	}

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	if err := scanner.Err; err != nil {
		panic(err)
	}
	return
}

// function to turn a slice of strings into a matrix
// if the seperator string is nil, it is assumed that each character
// is a single digit number
func ToMatrix(input []string, separator string) *mat.Dense {
	var stringInput [][]string
	for _, row := range input {
		var inputRow []string
		if separator == "" {
			inputRow := make([]string, len(row))
			for i, r := range row {
				inputRow[i] = string(r)
			}
		} else {
			for _, row := range input {
				inputRow = strings.Split(row, separator)
			}
		}
		stringInput = append(stringInput, inputRow)
	}

	height, width := len(stringInput), len(stringInput[0])
	var values []float64
	for _, row := range stringInput {
		for _, v := range row {
			f, err := strconv.ParseFloat(v, 10)
			if err != nil {
				panic(err)
			}
			values = append(values, f)
		}
	}
	return mat.NewDense(height, width, values)
}
