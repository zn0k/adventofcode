package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Claim struct {
	Id     int
	Left   int
	Top    int
	Width  int
	Height int
}

type Point struct {
	X int
	Y int
}

func ReadLines(path string) []Claim {
	f, err := os.Open(path)
	if err != nil {
		panic(fmt.Sprintf("unable to open %s for reading", path))
	}
	defer f.Close()

	var result []Claim
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		fields := strings.Fields(scanner.Text())
		id, _ := strconv.ParseInt(fields[0][1:], 10, 32)
		end := len(fields[2]) - 1
		offsets := strings.Split(fields[2][0:end], ",")
		left, _ := strconv.ParseInt(offsets[0], 10, 32)
		top, _ := strconv.ParseInt(offsets[1], 10, 32)
		dimensions := strings.Split(fields[3], "x")
		width, _ := strconv.ParseInt(dimensions[0], 10, 32)
		height, _ := strconv.ParseInt(dimensions[1], 10, 32)
		result = append(
			result,
			Claim{
				Id:     int(id),
				Left:   int(left),
				Top:    int(top),
				Width:  int(width),
				Height: int(height),
			},
		)
	}

	return result
}

func GetPoints(claim Claim) []Point {
	var result []Point
	for x := claim.Left; x < claim.Left+claim.Width; x += 1 {
		for y := claim.Top; y < claim.Top+claim.Height; y += 1 {
			result = append(result, Point{X: x, Y: y})
		}
	}

	return result
}

func main() {
	claims := ReadLines(os.Args[1])
	var fabric [1000][1000][]int
	for _, claim := range claims {
		for _, point := range GetPoints(claim) {
			fabric[point.Y][point.X] = append(fabric[point.Y][point.X], claim.Id)
		}
	}

	overlaps := make(map[int]bool)
	solution1 := 0
	for y := 0; y < 1000; y += 1 {
		for x := 0; x < 1000; x += 1 {
			if len(fabric[y][x]) > 1 {
				solution1 += 1
				for _, id := range fabric[y][x] {
					overlaps[id] = true
				}
			}
		}
	}
	fmt.Printf("Solution 1: %d\n", solution1)

	for _, claim := range claims {
		_, ok := overlaps[claim.Id]
		if !ok {
			fmt.Printf("Solution 2: %d\n", claim.Id)
			break
		}
	}
}
