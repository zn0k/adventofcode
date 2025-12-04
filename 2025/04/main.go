package main

import (
	"bufio"
	"fmt"
	"os"
)

type Coordinate struct {
	X int
	Y int
}

// naive function to handle errors by panicking
func check(e error) {
	if e != nil {
		panic(e)
	}
}

// read lines in a file into lists of runes
func readLines(f string) ([][]rune, error) {
	file, err := os.Open(f)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	// store each line as a list of runes
	var data [][]rune

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		runes := []rune(line)
		data = append(data, runes)
	}
	return data, scanner.Err()
}

// count the rolls accessible on the grid
// also return the coordinates of accessible roles
func count_accessible(data [][]rune) (count int, coordinates []Coordinate) {
	accessible := 0
	max_size := len(data) * len(data[0])
	cs := make([]Coordinate, 0, max_size)

	// walk the grid
	for x := 0; x < len(data[0]); x++ {
		for y := 0; y < len(data); y++ {
			if data[y][x] == '.' {
				// not a roll here, skip
				continue
			}
			rolls := 0
			// walk the roll's neighbors
			for _, dx := range []int{0, 1, -1} {
				for _, dy := range []int{0, 1, -1} {
					if dx == 0 && dy == 0 {
						// an offset of (0, 0) is the roll itself
						continue
					}
					// check that the neighbor is valid
					nx := x + dx
					ny := y + dy
					if nx < 0 || ny < 0 || nx >= len(data[0]) || ny >= len(data) {
						continue
					}
					if data[ny][nx] == '@' {
						// neighbor is a roll, count it
						rolls += 1
					}
				}
			}
			if rolls < 4 {
				// fewer than 4 rolls as neighbors, roll is accessible
				accessible += 1
				cs = append(cs, Coordinate{x, y})
			}
		}
	}
	return accessible, cs
}

func main() {
	// read in the data
	data, err := readLines("input.txt")
	check(err)

	// count the accessible roles for part 1
	accessible, coordinates := count_accessible(data)
	fmt.Printf("Solution 1: %d\n", accessible)

	// while there are accessible rolls
	for len(coordinates) > 0 {
		additional := 0
		// remove the ones from the last round
		for _, c := range coordinates {
			data[c.Y][c.X] = '.'
		}
		// and iterate, adding up as we go
		additional, coordinates = count_accessible(data)
		accessible += additional
	}
	fmt.Printf("Solution 2: %d\n", accessible)
}
