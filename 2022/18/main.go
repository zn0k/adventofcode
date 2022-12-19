package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

type TwoDim struct {
	a, b int
}

type Coordinate struct {
	x, y, z int
}

type Tracker struct {
	xs, ys, zs map[TwoDim]map[int]bool
}

func NewTracker() *Tracker {
	t := &Tracker{}
	t.xs = make(map[TwoDim]map[int]bool)
	t.ys = make(map[TwoDim]map[int]bool)
	t.zs = make(map[TwoDim]map[int]bool)
	return t
}

func (t *Tracker) Add(c Coordinate) {
	if _, ok := t.xs[TwoDim{c.y, c.z}]; !ok {
		t.xs[TwoDim{c.y, c.z}] = make(map[int]bool)
	}
	t.xs[TwoDim{c.y, c.z}][c.x] = true
	if _, ok := t.ys[TwoDim{c.x, c.z}]; !ok {
		t.ys[TwoDim{c.x, c.z}] = make(map[int]bool)
	}
	t.ys[TwoDim{c.x, c.z}][c.y] = true
	if _, ok := t.zs[TwoDim{c.x, c.y}]; !ok {
		t.zs[TwoDim{c.x, c.y}] = make(map[int]bool)
	}
	t.zs[TwoDim{c.x, c.y}][c.z] = true
}

func (t *Tracker) NeighborCount(c Coordinate) int {
	count := 0
	if _, ok := t.xs[TwoDim{c.y, c.z}][c.x+1]; ok {
		count += 1
	}
	if _, ok := t.xs[TwoDim{c.y, c.z}][c.x-1]; ok {
		count += 1
	}
	if _, ok := t.ys[TwoDim{c.x, c.z}][c.y+1]; ok {
		count += 1
	}
	if _, ok := t.ys[TwoDim{c.x, c.z}][c.y-1]; ok {
		count += 1
	}
	if _, ok := t.zs[TwoDim{c.x, c.y}][c.z+1]; ok {
		count += 1
	}
	if _, ok := t.zs[TwoDim{c.x, c.y}][c.z-1]; ok {
		count += 1
	}
	return count
}

func ReadInput(path string) (map[Coordinate]bool, Coordinate) {
	buf, _ := ioutil.ReadFile(path)
	cubes := make(map[Coordinate]bool)
	max := Coordinate{0, 0, 0}
	for _, line := range strings.Split(string(buf), "\n") {
		fields := strings.Split(line, ",")
		nums := make([]int, len(fields))
		for i := 0; i < len(fields); i += 1 {
			num, _ := strconv.Atoi(fields[i])
			nums[i] = num
		}
		if nums[0] > max.x {
			max.x = nums[0]
		}
		if nums[1] > max.y {
			max.y = nums[1]
		}
		if nums[2] > max.z {
			max.z = nums[2]
		}
		cubes[Coordinate{nums[0], nums[1], nums[2]}] = true
	}
	return cubes, max
}

func main() {
	cubes, max := ReadInput(os.Args[1])
	tracker := NewTracker()
	for cube := range cubes {
		tracker.Add(cube)
	}

	neighbors := 0
	for cube := range cubes {
		neighbors += tracker.NeighborCount(cube)
	}

	part1 := (len(cubes) * 6) - neighbors
	fmt.Printf("Solution 1: %d\n", part1)

	// note for future me for part 2
	// use the below to create a cube one bigger than the maxes below
	fmt.Printf("%v\n", max)
	// from there, pick a boundary air from the bottom back right, guaranteed to not be magma
	// then run a DFS or BFS fill to find all neighbors that can be reached that are not magma
	// then run through all of the air cubes and call NeighborCount, which should enumerate the solution
}
