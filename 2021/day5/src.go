package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Coordinate struct {
	x int
	y int
}

type Line struct {
	from Coordinate
	to   Coordinate
}

func readLines(path string) ([]Line, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var coordinates []Line

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		fields := strings.Fields(line)
		vals := strings.Split(fields[0], ",")
		vals = append(vals, strings.Split(fields[2], ",")...)
		var intVals []int
		for _, val := range vals {
			i, err := strconv.ParseInt(val, 10, 32)
			if err != nil {
				return nil, err
			}
			intVals = append(intVals, int(i))
		}
		from := Coordinate{intVals[0], intVals[1]}
		to := Coordinate{intVals[2], intVals[3]}

		coordinates = append(coordinates, Line{from, to})
	}

	return coordinates, scanner.Err()
}

func printBoard(board *[][]int) {
	for _, line := range *board {
		fmt.Printf("%v\n", line)
	}
	fmt.Printf("\n")
}

func linePoints(line Line) []Coordinate {
	var coordinates []Coordinate

	// vertical
	if line.from.x == line.to.x {
		if line.from.y < line.to.y {
			for y := line.from.y; y <= line.to.y; y++ {
				coordinates = append(coordinates, Coordinate{line.from.x, y})
			}
		} else {
			for y := line.from.y; y >= line.to.y; y-- {
				coordinates = append(coordinates, Coordinate{line.from.x, y})
			}
		}
		return coordinates
	}
	// horizontal
	if line.from.y == line.to.y {
		if line.from.x < line.to.x {
			for x := line.from.x; x <= line.to.x; x++ {
				coordinates = append(coordinates, Coordinate{x, line.from.y})
			}
		} else {
			for x := line.from.x; x >= line.to.x; x-- {
				coordinates = append(coordinates, Coordinate{x, line.from.y})
			}
		}
		return coordinates
	}
	// diagonal
	var xs, ys []int
	if line.from.x < line.to.x {
		for x := line.from.x; x <= line.to.x; x++ {
			xs = append(xs, x)
		}
	} else {
		for x := line.from.x; x >= line.to.x; x-- {
			xs = append(xs, x)
		}
	}
	if line.from.y < line.to.y {
		for y := line.from.y; y <= line.to.y; y++ {
			ys = append(ys, y)
		}
	} else {
		for y := line.from.y; y >= line.to.y; y-- {
			ys = append(ys, y)
		}
	}
	for i := 0; i < len(xs); i++ {
		coordinates = append(coordinates, Coordinate{xs[i], ys[i]})
	}
	return coordinates
}

func scoreBoard(board *[][]int) int {
	result := 0
	for _, line := range *board {
		for _, val := range line {
			if val >= 2 {
				result++
			}
		}
	}
	return result
}

func main() {
	lines, err := readLines(os.Args[1])
	if err != nil {
		panic(err)
	}

	height, width := 0, 0
	for _, line := range lines {
		if line.from.x > width {
			width = line.from.x
		}
		if line.from.y > height {
			height = line.from.y
		}
		if line.to.x > width {
			width = line.to.x
		}
		if line.to.y > height {
			height = line.to.y
		}
	}
	height += 1
	width += 1

	var board [][]int
	for i := 0; i < height; i++ {
		board = append(board, make([]int, width))
	}

	var horizontal_vertical, diagonal []Line
	for _, line := range lines {
		if line.from.x == line.to.x || line.from.y == line.to.y {
			horizontal_vertical = append(horizontal_vertical, line)
		} else {
			diagonal = append(diagonal, line)
		}
	}

	for _, line := range horizontal_vertical {
		for _, coordinate := range linePoints(line) {
			board[coordinate.y][coordinate.x]++
		}
	}
	fmt.Printf("Solution 1: %d\n", scoreBoard(&board))

	for _, line := range diagonal {
		for _, coordinate := range linePoints(line) {
			board[coordinate.y][coordinate.x]++
		}
	}
	fmt.Printf("Solution 2: %d\n", scoreBoard(&board))
}
