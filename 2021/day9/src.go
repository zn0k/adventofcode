package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

type Coordinate struct {
	x int
	y int
}

type Neighbors []Coordinate

type Point struct {
	height    int
	neighbors Neighbors
}

type Map [][]Point

func readLines(path string) ([][]int, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var points [][]int

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		var row []int
		for _, c := range line {
			i, err := strconv.ParseInt(string(c), 10, 32)
			if err != nil {
				return nil, err
			}
			row = append(row, int(i))
		}
		points = append(points, row)
	}
	return points, scanner.Err()
}

func getNeighbors(c Coordinate, width int, height int) Neighbors {
	var neighbors Neighbors
	if c.x > 0 {
		neighbors = append(neighbors, Coordinate{c.x - 1, c.y})
	}
	if c.x < width {
		neighbors = append(neighbors, Coordinate{c.x + 1, c.y})
	}
	if c.y > 0 {
		neighbors = append(neighbors, Coordinate{c.x, c.y - 1})
	}
	if c.y < height {
		neighbors = append(neighbors, Coordinate{c.x, c.y + 1})
	}
	return neighbors
}

func minMax(xs []int) (int, int) {
	min, max := xs[0], xs[0]
	for _, x := range xs {
		if x < min {
			min = x
		}
		if x > max {
			max = x
		}
	}
	return min, max
}

func main() {
	points, err := readLines(os.Args[1])
	if err != nil {
		panic(err)
	}

	height := len(points) - 1
	width := len(points[0]) - 1

	var lowest []Coordinate
	for y, row := range points {
		for x, p := range row {
			var heights []int
			for _, n := range getNeighbors(Coordinate{x, y}, width, height) {
				heights = append(heights, points[n.y][n.x])
			}
			min, _ := minMax(heights)
			if p <= min {
				lowest = append(lowest, Coordinate{x, y})
			}
		}
	}

	//sum := 0
	//for _, i := range lowest {
	//	sum += i + 1
	//}
	for _, p := range lowest {
		fmt.Printf("%d,%d\n", p.x, p.y)
	}
	fmt.Printf("Solution 1: %v\n", lowest)
}
