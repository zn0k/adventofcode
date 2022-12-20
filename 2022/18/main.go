package main

import (
	"container/list"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

type Coordinate struct {
	x, y, z int
}

type Tracker struct {
	m map[Coordinate]bool
}

func NewTracker() *Tracker {
	t := &Tracker{}
	t.m = make(map[Coordinate]bool)
	return t
}

func (t *Tracker) Add(c Coordinate) {
	t.m[c] = true
}

func (t *Tracker) NeighborCount(c Coordinate) int {
	count := 0
	if _, ok := t.m[Coordinate{c.x, c.y, c.z + 1}]; ok {
		count += 1
	}
	if _, ok := t.m[Coordinate{c.x, c.y, c.z - 1}]; ok {
		count += 1
	}
	if _, ok := t.m[Coordinate{c.x, c.y + 1, c.z}]; ok {
		count += 1
	}
	if _, ok := t.m[Coordinate{c.x, c.y - 1, c.z}]; ok {
		count += 1
	}
	if _, ok := t.m[Coordinate{c.x + 1, c.y, c.z}]; ok {
		count += 1
	}
	if _, ok := t.m[Coordinate{c.x - 1, c.y, c.z}]; ok {
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

func GenerateNeighbor(c Coordinate, max Coordinate) []Coordinate {
	neighbors := make([]Coordinate, 0)
	for _, o := range []Coordinate{{0, 0, 1}, {0, 0, -1}, {0, 1, 0}, {0, -1, 0}, {1, 0, 0}, {-1, 0, 0}} {
		candidate := Coordinate{c.x + o.x, c.y + o.y, c.z + o.z}
		if candidate.x < 0 || candidate.x > max.x {
			continue
		}
		if candidate.y < 0 || candidate.y > max.y {
			continue
		}
		if candidate.z < 0 || candidate.z > max.z {
			continue
		}
		neighbors = append(neighbors, candidate)
	}
	return neighbors
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

	// BFS for air from the boundary in
	max = Coordinate{max.x + 1, max.y + 1, max.z + 1}
	air := make(map[Coordinate]bool)
	q := list.New()
	q.PushBack(max)
	air[max] = true
	for q.Front() != nil {
		current := q.Front()
		q.Remove(current)
		for _, n := range GenerateNeighbor(current.Value.(Coordinate), max) {
			if _, seen := air[n]; seen {
				continue
			}
			if _, lava := tracker.m[n]; lava {
				continue
			}
			air[n] = true
			q.PushBack(n)
		}
	}

	// get all trapped air (= all cubes not in lava or BFS filled air)
	var trapped []Coordinate
	for x := 0; x < max.x; x += 1 {
		for y := 0; y < max.y; y += 1 {
			for z := 0; z < max.z; z += 1 {
				c := Coordinate{x, y, z}
				if _, air := air[c]; air {
					continue
				}
				if _, lava := tracker.m[c]; lava {
					continue
				}
				trapped = append(trapped, c)
			}
		}
	}
	// count up the lava surfaces for trapped air, subtract it from part 1
	inside := 0
	for _, t := range trapped {
		inside += tracker.NeighborCount(t)
	}
	fmt.Printf("Solution 2: %d\n", part1-inside)
}
