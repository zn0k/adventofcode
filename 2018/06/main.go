package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

type Point struct {
	X, Y int
}

func (p *Point) Distance(other Point) int {
	return Abs(p.X-other.X) + Abs(p.Y-other.Y)
}

func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

type Tracker struct {
	Min, MinNext int
	Index        int
}

func (t *Tracker) Record(distance, index int) {
	if distance < t.Min {
		t.MinNext = t.Min
		t.Min = distance
		t.Index = index
	} else if distance < t.MinNext {
		t.MinNext = distance
	}
}

func (t *Tracker) MinIndex() int {
	if t.Min == t.MinNext {
		return -1
	}
	return t.Index
}

func NewTracker() *Tracker {
	t := &Tracker{}
	t.Min = math.MaxInt32
	t.MinNext = math.MaxInt32
	t.Index = -1
	return t
}

func ReadInput(path string) []Point {
	f, err := os.Open(path)
	if err != nil {
		panic(fmt.Sprintf("unable to open %s for reading", path))
	}
	defer f.Close()

	var points []Point

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		fields := strings.Split(scanner.Text(), ", ")
		x, _ := strconv.Atoi(fields[0])
		y, _ := strconv.Atoi(fields[1])
		points = append(points, Point{X: x, Y: y})
	}

	return points
}

func GetDimensions(points []Point) (width, height int) {
	for _, p := range points {
		if p.X > width {
			width = p.X
		}
		if p.Y > height {
			height = p.Y
		}
	}

	return
}

func CalculateClosest(board [][]int, points []Point) int {
	height := len(board)
	width := len(board[0])

	for y := 0; y < height; y += 1 {
		for x := 0; x < width; x += 1 {
			tracker := NewTracker()
			point := Point{X: x, Y: y}
			for i, p := range points {
				distance := p.Distance(point)
				tracker.Record(distance, i)
			}

			board[y][x] = tracker.MinIndex()
		}
	}

	tracker := make(map[int]int, len(points))

	for y := 0; y < height; y += 1 {
		for x := 0; x < width; x += 1 {
			closest := board[y][x]
			tracker[closest] += 1
		}
	}

	// remove all counts for points that are present on the edge of the board
	// those points extend to infinity and should not count
	for _, y := range []int{0, height - 1} {
		for x := 0; x < width; x += 1 {
			closest := board[y][x]
			tracker[closest] = 0
		}
	}
	for _, x := range []int{0, width - 1} {
		for y := 0; y < height; y += 1 {
			closest := board[y][x]
			tracker[closest] = 0
		}
	}

	max := 0
	for _, count := range tracker {
		if count > max {
			max = count
		}
	}

	return max
}

func CalculateSafest(board [][]int, points []Point) int {
	height := len(board)
	width := len(board[0])

	for y := 0; y < height; y += 1 {
		for x := 0; x < width; x += 1 {
			sum := 0
			point := Point{X: x, Y: y}
			for _, p := range points {
				distance := p.Distance(point)
				sum += distance
			}
			if sum < 10000 {
				board[y][x] = 1
			}
		}
	}

	size := 0
	for y := 0; y < height; y += 1 {
		for x := 0; x < width; x += 1 {
			size += board[y][x]
		}
	}

	return size
}

func main() {
	points := ReadInput(os.Args[1])

	width, height := GetDimensions(points)

	board := make([][]int, height+1)
	for y := 0; y < height+1; y += 1 {
		row := make([]int, width+1)
		board[y] = row
	}

	closest := CalculateClosest(board, points)

	fmt.Printf("Solution 1: %d\n", closest)

	board = make([][]int, height+1)
	for y := 0; y < height+1; y += 1 {
		row := make([]int, width+1)
		board[y] = row
	}

	safest := CalculateSafest(board, points)

	fmt.Printf("Solution 2: %d\n", safest)
}
