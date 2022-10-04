package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
)

type Set struct {
	m map[rune]bool
}

func (s *Set) Add(v rune) {
	s.m[v] = true
}

func (s *Set) Contains(v rune) bool {
	_, c := s.m[v]
	return c
}

func NewSet() *Set {
	s := &Set{}
	s.m = make(map[rune]bool)
	return s
}

func readLines(p string) ([]string, error) {
	file, err := os.Open(p)
	if err != nil {
		return nil, err
	}

	var lines []string

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines, scanner.Err()
}

func main() {
	lines, err := readLines(os.Args[1])
	if err != nil {
		panic(err)
	}

	pairs := make(map[rune]rune)
	pairs['('] = ')'
	pairs['{'] = '}'
	pairs['['] = ']'
	pairs['<'] = '>'

	illegal_scores := make(map[rune]int)
	illegal_scores[')'] = 3
	illegal_scores[']'] = 57
	illegal_scores['}'] = 1197
	illegal_scores['>'] = 25137

	completion_scores := make(map[rune]int)
	completion_scores['('] = 1
	completion_scores['['] = 2
	completion_scores['{'] = 3
	completion_scores['<'] = 4

	open, close := NewSet(), NewSet()
	for k, v := range pairs {
		open.Add(k)
		close.Add(v)
	}

	var stack []rune

	illegal_score := 0
	var candidates []int
	for _, line := range lines {
		for _, r := range line {
			if open.Contains(r) {
				stack = append(stack, r)
			} else if close.Contains(r) {
				var last rune
				last, stack = stack[len(stack)-1], stack[:len(stack)-1]
				if pairs[last] != r {
					illegal_score += illegal_scores[r]
					stack = []rune{}
					break
				}
			}
		}
		if len(stack) > 0 {
			score := 0
			for i := len(stack) - 1; i >= 0; i-- {
				score = score*5 + completion_scores[stack[i]]
			}
			candidates = append(candidates, score)
		}
		stack = []rune{}
	}

	sort.Ints(candidates)

	fmt.Printf("Solution 1: %d\n", illegal_score)
	fmt.Printf("Solution 2: %d\n", candidates[len(candidates)/2])
}
