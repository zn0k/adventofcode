package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"strconv"
	"strings"
)

type World [][]int
type Coordinate struct {
	X, Y int
}

func ReadInput(path string) World {
	buf, err := ioutil.ReadFile(path)
	if err != nil {
		panic(fmt.Sprintf("unable to read from %s", path))
	}
	lines := strings.Split(string(buf), "\n")

	var world World
	for _, line := range lines {
		var nums []int
		for _, c := range line {
			i, _ := strconv.Atoi(string(c))
			nums = append(nums, i)
		}
		world = append(world, nums)
	}
	return world
}

func FindHighPoints(world World) int {
	height := len(world)
	width := len(world[0])
	tracker := make(map[Coordinate]bool)

	// by row, left to right, track each coordinate that has the
	// max height so far from that direction
	for y := 0; y < height; y += 1 {
		max_left, max_right := -1, -1
		for x := 0; x < width && (max_left < 9 || max_right < 9); x += 1 {
			if world[y][x] > max_left {
				max_left = world[y][x]
				tracker[Coordinate{X: x, Y: y}] = true
			}
			if world[y][width-1-x] > max_right {
				max_right = world[y][width-1-x]
				tracker[Coordinate{X: width - 1 - x, Y: y}] = true
			}
		}
	}
	// now go column by column, top down
	for x := 0; x < width; x += 1 {
		max_down, max_up := -1, -1
		for y := 0; y < height && (max_up < 9 || max_down < 9); y += 1 {
			if world[y][x] > max_down {
				max_down = world[y][x]
				tracker[Coordinate{X: x, Y: y}] = true
			}
			if world[height-1-y][x] > max_up {
				max_up = world[height-1-y][x]
				tracker[Coordinate{X: x, Y: height - 1 - y}] = true
			}
		}
	}

	var result []Coordinate
	for key := range tracker {
		result = append(result, key)
	}
	return len(result)
}

func MaxScore(world World) int {
	height := len(world)
	width := len(world[0])

	var scores []int

	// for each coordinate, calculate its view score and record it
	// ignore edges since their total score must always be 0
	for y := 1; y < height-1; y += 1 {
		for x := 1; x < width-1; x += 1 {
			up, down, left, right := 0, 0, 0, 0
			// go up
			for offset_y := y - 1; offset_y >= 0; offset_y -= 1 {
				up += 1
				if world[offset_y][x] >= world[y][x] {
					break
				}
			}
			// go down
			for offset_y := y + 1; offset_y < height; offset_y += 1 {
				down += 1
				if world[offset_y][x] >= world[y][x] {
					break
				}
			}
			// go left
			for offset_x := x - 1; offset_x >= 0; offset_x -= 1 {
				left += 1
				if world[y][offset_x] >= world[y][x] {
					break
				}
			}
			// go right
			for offset_x := x + 1; offset_x < width; offset_x += 1 {
				right += 1
				if world[y][offset_x] >= world[y][x] {
					break
				}
			}
			scores = append(scores, up*down*left*right)
		}
	}

	sort.Ints(scores)
	return scores[len(scores)-1]
}

func main() {
	world := ReadInput(os.Args[1])
	fmt.Printf("Solution 1: %d\n", FindHighPoints(world))
	fmt.Printf("Solutuon 2: %d\n", MaxScore(world))
}
