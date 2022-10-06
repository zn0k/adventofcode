package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Counter struct {
	m map[string]int64
}

func (c *Counter) Add(k string, v int64) {
	if _, exists := c.m[k]; exists {
		c.m[k] += v
	} else {
		c.m[k] = v
	}
}

func (c *Counter) Subtract(k string, v int64) {
	if _, exists := c.m[k]; exists {
		c.m[k] -= v
	} else {
		c.m[k] = -v
	}
}

func (c *Counter) Score() int64 {
	var min, max int64
	min, max = 0, 0
	for _, v := range c.m {
		if v < min || min == 0 {
			min = v
		}
		if v > max || max == 0 {
			max = v
		}
	}
	return max - min
}

func NewCounter() Counter {
	c := &Counter{}
	c.m = make(map[string]int64)
	return *c
}

func readLines(p string) (seed string, rules map[string]string, err error) {
	f, err := os.Open(p)
	if err != nil {
		return "", nil, err
	}
	rules = make(map[string]string)
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := scanner.Text()
		if len(line) == 0 {
			continue
		}
		if strings.Contains(line, "->") {
			fields := strings.Split(line, " -> ")
			rules[fields[0]] = fields[1]
		} else {
			seed = line
		}
	}
	err = scanner.Err()
	return
}

func main() {
	seed, rules, err := readLines(os.Args[1])
	if err != nil {
		panic(err)
	}

	var letters []string
	for _, r := range seed {
		letters = append(letters, string(r))
	}
	counter := NewCounter()
	pairs := NewCounter()
	for i := 0; i < len(letters)-1; i++ {
		pair := letters[i] + letters[i+1]
		pairs.Add(pair, 1)
		counter.Add(letters[i], 1)
	}
	counter.Add(letters[len(letters)-1], 1)

	for i := 0; i < 40; i++ {
		current := make(map[string]int64)
		for pair, count := range pairs.m {
			current[pair] = count
		}
		for pair, count := range current {
			new := rules[pair]
			left := pair[0:1] + new
			right := new + pair[1:]
			pairs.Subtract(pair, count)
			pairs.Add(left, count)
			pairs.Add(right, count)
			counter.Add(new, count)
		}
		if i == 9 {
			fmt.Printf("Solution 1: %d\n", counter.Score())
		}
	}
	fmt.Printf("Solution 2: %d\n", counter.Score())
}
