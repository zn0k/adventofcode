package main

import (
	"bufio"
	"os"
	"strconv"
	"strings"
)

type Up int64
type Down int64
type Forward int64

type Direction interface {
	Up | Down | Forward
}

func readLines[T Direction](path string) ([]T, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []T

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		words := strings.Fields(scanner.Text())
		i, err := strconv.ParseInt(words[1], 10, 64)
		if err != nil {
			continue
		}

		switch words[0] {
		case "up":
			var direction Up = Up(i)
			lines = append(lines, direction)
		}

	}
	return lines, scanner.Err()
}

func main() {

}
