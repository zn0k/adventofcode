package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Note struct {
	inputs  []string
	outputs []string
}

func readLines(path string) ([]Note, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var notes []Note

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		parts := strings.Split(line, " | ")
		inputFields := strings.Fields(parts[0])
		outputFields := strings.Fields(parts[1])
		notes = append(notes, Note{inputFields, outputFields})
	}

	return notes, scanner.Err()
}

func getCounts(s string) map[string]int {
	counts := make(map[string]int)

	for _, key := range "abcdefg" {
		count := 0
		for _, c := range s {
			if key == c {
				count++
			}
		}
		counts[string(key)] = count
	}
	return counts
}

func makeKey(s string, counts map[string]int) string {
	var stringified []string
	for _, c := range s {
		count := counts[string(c)]
		stringified = append(stringified, strconv.FormatInt(int64(count), 10))
	}
	sort.Strings(stringified)
	return strings.Join(stringified, "")
}

func translate(note Note, lookup map[string]string) string {
	concat := ""
	for _, input := range note.inputs {
		concat += input
	}

	counts := getCounts(concat)

	result := ""
	for _, output := range note.outputs {
		key := makeKey(output, counts)
		result += lookup[key]
	}
	return result
}

func main() {
	notes, err := readLines(os.Args[1])
	if err != nil {
		panic(err)
	}

	digits := map[string]string{
		"0": "abcefg",
		"1": "cf",
		"2": "acdeg",
		"3": "acdfg",
		"4": "bcdf",
		"5": "abdfg",
		"6": "abdefg",
		"7": "acf",
		"8": "abcdefg",
		"9": "abcdfg",
	}

	concat := ""
	for _, v := range digits {
		concat += v
	}

	counts := getCounts(concat)

	lookups := make(map[string]string)
	for digit, value := range digits {
		key := makeKey(value, counts)
		lookups[key] = digit
	}

	var translated []string
	for _, note := range notes {
		translated = append(translated, translate(note, lookups))
	}

	solution1 := 0
	for _, x := range translated {
		for _, c := range x {
			s := string(c)
			if s == "1" || s == "4" || s == "7" || s == "8" {
				solution1++
			}
		}
	}
	fmt.Printf("Solution 1: %d\n", solution1)

	solution2 := 0
	for _, x := range translated {
		i, err := strconv.ParseInt(x, 10, 32)
		if err != nil {
			panic(err)
		}
		solution2 += int(i)
	}
	fmt.Printf("Solution 2: %d\n", solution2)
}
