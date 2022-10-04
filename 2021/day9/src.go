package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
)

type Coordinate struct {
	x int
	y int
}

type Neighbors []Coordinate

type Map [][]int

type Set struct {
	m map[Coordinate]bool
}

func (s *Set) Add(v Coordinate) {
	s.m[v] = true
}

func (s *Set) Remove(v Coordinate) {
	delete(s.m, v)
}

func (s *Set) Contains(v Coordinate) bool {
	_, ok := s.m[v]
	return ok
}

func NewSet() *Set {
	s := &Set{}
	s.m = make(map[Coordinate]bool)
	return s
}

func readLines(path string) (Map, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var points Map

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

func getNeighbors(p Coordinate, m *Map) Neighbors {
	width, height := getDimensions(m)
	var neighbors Neighbors
	if p.x > 0 {
		neighbors = append(neighbors, Coordinate{p.x - 1, p.y})
	}
	if p.x < width {
		neighbors = append(neighbors, Coordinate{p.x + 1, p.y})
	}
	if p.y > 0 {
		neighbors = append(neighbors, Coordinate{p.x, p.y - 1})
	}
	if p.y < height {
		neighbors = append(neighbors, Coordinate{p.x, p.y + 1})
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

func getDimensions(m *Map) (int, int) {
	height := len(*m) - 1
	width := len((*m)[0]) - 1
	return width, height
}

func getBasinSize(p Coordinate, m *Map) int {
	seen := NewSet()
	candidates := []Coordinate{p}
	size := 0

	for len(candidates) > 0 {
		size += 1
		next := candidates[0]
		candidates = candidates[1:]
		seen.Add(next)
		for _, n := range getNeighbors(next, m) {
			if !seen.Contains(n) && (*m)[n.y][n.x] != 9 {
				candidates = append(candidates, n)
				seen.Add(n)
			}
		}
	}

	return size
}

func main() {
	points, err := readLines(os.Args[1])
	if err != nil {
		panic(err)
	}

	var lowest []Coordinate
	for y, row := range points {
		for x, p := range row {
			var heights []int
			for _, n := range getNeighbors(Coordinate{x, y}, &points) {
				heights = append(heights, points[n.y][n.x])
			}
			min, _ := minMax(heights)
			if p < min {
				lowest = append(lowest, Coordinate{x, y})
			}
		}
	}

	sum := 0
	basinSizes := []int{}
	for _, p := range lowest {
		sum += points[p.y][p.x] + 1
		basinSizes = append(basinSizes, getBasinSize(p, &points))
	}
	sort.Ints(basinSizes)
	l := len(basinSizes)
	solution2 := basinSizes[l-3] * basinSizes[l-2] * basinSizes[l-1]

	fmt.Printf("Solution 1: %d\n", sum)
	fmt.Printf("Solution 2: %d\n", solution2)
}
