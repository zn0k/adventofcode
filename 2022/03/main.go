package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"unicode"
)

func ReadLines(path string) []string {
	buf, err := ioutil.ReadFile(path)
	if err != nil {
		panic(fmt.Sprintf("unable to read %s", path))
	}

	return strings.Split(string(buf), "\n")
}

func FindRepeat(input []string) string {
	var repeat string
	for _, letter := range strings.Split(input[0], "") {
		match := true
		for _, line := range input {
			if strings.Count(line, letter) == 0 {
				match = false
			}
		}
		if match {
			repeat = letter
			break
		}
	}
	return repeat
}

func FindItems(input []string) []string {
	var doubles []string

	for _, line := range input {
		a := line[:len(line)/2]
		b := line[len(line)/2:]
		doubles = append(doubles, FindRepeat([]string{a, b}))
	}

	return doubles
}

func FindBadges(input []string) []string {
	var badges []string

	for i := 0; i < len(input); i += 3 {
		badges = append(badges, FindRepeat([]string{input[i], input[i+1], input[i+2]}))
	}

	return badges
}

func Score(input []string) int {
	total := 0
	for _, item := range input {
		letter := rune(item[0])
		if unicode.IsLower(letter) {
			total += int(letter) - 96
		} else {
			total += int(letter) - 64 + 26
		}
	}
	return total
}

func main() {
	lines := ReadLines(os.Args[1])
	doubles := FindItems(lines)
	score := Score(doubles)
	fmt.Printf("Solution 1: %d\n", score)

	badges := FindBadges(lines)
	score = Score(badges)
	fmt.Printf("Solution 2: %d\n", score)
}
