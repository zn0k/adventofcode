package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func readLines(path string) ([]string, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var vals []string

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		vals = append(vals, line)
	}
	return vals, scanner.Err()
}

func findMostCommonBit(vals []string, pos int) string {
	bits := ""
	for _, val := range vals {
		bits += string(val[pos])
	}
	ones := strings.Count(bits, "1")
	zeroes := len(bits) - ones

	if zeroes > ones {
		return "0"
	}
	return "1"
}

func negateBinaryString(val string) string {
	result := ""
	for _, val := range val {
		if string(val) == "0" {
			result += "1"
		} else {
			result += "0"
		}
	}
	return result
}

func binaryStringToInt(val string) int {
	length := len(val)
	result := 0
	for i, char := range val {
		if string(char) == "1" {
			result += 1 << (length - i - 1)
		}
	}
	return result
}

func removeFromSlice(s []int, i int) []int {
	s[i] = s[len(s)-1]
	return s[:len(s)-1]
}

func filterVals(vals []string, cmp string, pos int) []string {
	var filtered []string
	for _, val := range vals {
		if string(val[pos]) == cmp {
			filtered = append(filtered, val)
		}
	}
	return filtered
}

func findVal(vals []string, most bool) string {
	pos := 0
	filtered := vals
	for len(filtered) > 1 {
		cmp := findMostCommonBit(filtered, pos)
		if !most {
			if cmp == "1" {
				cmp = "0"
			} else {
				cmp = "1"
			}
		}
		filtered = filterVals(filtered, cmp, pos)
		pos += 1
	}
	return filtered[0]
}

func main() {
	vals, err := readLines(os.Args[1])
	if err != nil {
		panic(err)
	}

	gamma := ""
	for i := 0; i < len(vals[0]); i++ {
		gamma += findMostCommonBit(vals, i)
	}
	epsilon := negateBinaryString(gamma)
	fmt.Printf("Solution 1: %d\n", binaryStringToInt(gamma)*binaryStringToInt(epsilon))

	o2 := findVal(vals, true)
	co2 := findVal(vals, false)
	fmt.Printf("Soltution 2: %d\n", binaryStringToInt(o2)*binaryStringToInt(co2))
}
