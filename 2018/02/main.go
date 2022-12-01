package main

import (
	"bufio"
	"fmt"
	"os"
)

func getLines(path string) []string {
	f, err := os.Open(path)
	if err != nil {
		panic(fmt.Sprintf("unable to open %s for reading", path))
	}
	defer f.Close()

	var result []string
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		result = append(result, scanner.Text())
	}

	return result
}

func countLetters(line string) map[string]int {
	result := make(map[string]int)
	for _, r := range line {
		c := string(r)
		_, ok := result[c]
		if ok {
			result[c] += 1
		} else {
			result[c] = 1
		}
	}

	return result
}

func hasX(in map[string]int, x int) bool {
	for _, count := range in {
		if count == x {
			return true
		}
	}

	return false
}

func hasTwo(in map[string]int) bool   { return hasX(in, 2) }
func hasThree(in map[string]int) bool { return hasX(in, 3) }

func commonLetters(line1, line2 string) string {
	common := ""
	for i := 0; i < len(line1); i += 1 {
		if line1[i] == line2[i] {
			common += string(line1[i])
		}
	}

	return common
}

func main() {
	lines := getLines(os.Args[1])

	twos := 0
	threes := 0
	for _, line := range lines {
		indexedLine := countLetters(line)
		if hasTwo(indexedLine) {
			twos += 1
		}
		if hasThree(indexedLine) {
			threes += 1
		}
	}

	fmt.Printf("Solution 1: %d\n", twos*threes)

DONE:
	for _, line1 := range lines {
		for _, line2 := range lines {
			if line1 == line2 {
				continue
			}
			common := commonLetters(line1, line2)
			if len(common) == len(line1)-1 {
				fmt.Printf("Solution 2: %s\n", common)
				break DONE
			}
		}
	}
}
