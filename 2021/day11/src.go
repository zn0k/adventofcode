package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

type Map [][]int

type Coordinate struct {
	x, y int
}

func readLines(p string) (Map, error) {
	file, err := os.Open(p)
	if err != nil {
		return nil, err
	}

	var m Map

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		var row []int
		line := scanner.Text()
		for _, r := range line {
			i, err := strconv.ParseInt(string(r), 10, 32)
			if err != nil {
				return nil, err
			}
			row = append(row, int(i))
		}
		m = append(m, row)
	}
	return m, scanner.Err()
}

func getDimensions(m *Map) (width, height int) {
	height = len(*m) - 1
	width = len((*m)[0]) - 1
	return
}

func getNeighbors(c Coordinate, m *Map) []Coordinate {
	width, height := getDimensions(m)
	offsets := []Coordinate{{-1, -1}, {0, -1}, {1, -1}, {-1, 0}, {1, 0}, {-1, 1}, {0, 1}, {1, 1}}

	var neighbors []Coordinate
	for _, o := range offsets {
		candidate := Coordinate{c.x + o.x, c.y + o.y}
		if candidate.x >= 0 && candidate.x <= width && candidate.y >= 0 && candidate.y <= height {
			neighbors = append(neighbors, candidate)
		}
	}
	return neighbors
}

func all(cmp int, m *Map) bool {
	for _, row := range *m {
		for _, v := range row {
			if v != cmp {
				return false
			}
		}
	}
	return true
}

func increaseEngergy(m *Map) {
	width, height := getDimensions(m)
	for y := 0; y <= height; y++ {
		for x := 0; x <= width; x++ {
			(*m)[y][x] += 1
		}
	}
}

func zeroes(width, height int) Map {
	var zeroes [][]int
	for i := 0; i <= height; i++ {
		row := make([]int, width+1)
		zeroes = append(zeroes, row)
	}
	return zeroes
}

func printWorld(m *Map) {
	for _, row := range *m {
		fmt.Printf("%v\n", row)
	}
	fmt.Printf("\n")
}

func main() {
	world, err := readLines(os.Args[1])
	if err != nil {
		panic(err)
	}

	//printWorld(&world)
	width, height := getDimensions(&world)
	total_flashes, step := 0, 0
	for {
		step += 1
		increaseEngergy(&world)
		flashed := zeroes(width, height)
		keep_looping := true
		//printWorld(&world)
		for keep_looping {
			keep_looping = false
			for y := 0; y <= height; y++ {
				for x := 0; x <= width; x++ {
					if world[y][x] > 9 && flashed[y][x] == 0 {
						for _, n := range getNeighbors(Coordinate{x, y}, &world) {
							world[n.y][n.x]++
						}
						flashed[y][x] = 1
						keep_looping = true
						if step <= 100 {
							total_flashes++
						}
					}
				}
			}
		}
		for y := 0; y <= height; y++ {
			for x := 0; x <= width; x++ {
				if flashed[y][x] == 1 {
					world[y][x] = 0
				}
			}
		}
		//printWorld(&world)
		if all(0, &world) {
			break
		}
	}
	fmt.Printf("Solution 1: %d\nSolution 2: %d\n", total_flashes, step)
}
