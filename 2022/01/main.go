package main

import (
	"bufio"
	"fmt"
	"os"
)

func readInput(path string) []string {
	f, err := os.Open(path)
	if err != nil {
		panic(fmt.Sprintf("unable to open %s for reading", path))
	}
	defer f.Close()

	var lines []string
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := scanner.Text()
		lines = append(lines, line)
	}

	return lines
}

func main() {
	input := readInput(os.Args[1])
	fmt.Printf("%v", input)
}
