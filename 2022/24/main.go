package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"strings"
)

type Coordinate struct {
	x, y int
}

// a given state of blizzards on the map, mapping a coordinate to
// a list of strings, each corresponding to a blizzard or a wall
type Blizzard map[Coordinate][]string

// a list of such states, indexed by their timestamp
type Blizzards []map[Coordinate][]string

func ReadInput(path string) (Blizzards, int, int) {
	buf, _ := ioutil.ReadFile(path)
	lines := strings.Split(string(buf), "\n")
	height, width := len(lines)-1, len(lines[0])-1
	blizzards := make(Blizzards, height*width)
	// initial state is at timestamp 0
	blizzards[0] = make(Blizzard)
	// parse the input into a set of coordinates where walls and blizzards are
	for y := 0; y <= height; y += 1 {
		chars := strings.Split(lines[y], "")
		for x := 0; x <= width; x += 1 {
			if chars[x] == "." {
				continue
			} else {
				blizzards[0][Coordinate{x, y}] = []string{chars[x]}
			}
		}
	}
	// initial state is now encoded, calculate forward states
	// do this (width * height) times, which is where the state will cycle
	for i := 1; i < width*height; i += 1 {
		blizzards[i] = make(Blizzard)
		for c, d := range blizzards[i-1] {
			for _, b := range d { // can have multiple blizzards at same coordinate
				var new Coordinate
				switch b {
				// go through directions, preserving blizzard energy by pac-man'ing them
				case ">":
					new = Coordinate{c.x + 1, c.y}
					if new.x > width-1 {
						new.x = 1
					}
				case "v":
					new = Coordinate{c.x, c.y + 1}
					if new.y > height-1 {
						new.y = 1
					}
				case "<":
					new = Coordinate{c.x - 1, c.y}
					if new.x < 1 {
						new.x = width - 1
					}
				case "^":
					new = Coordinate{c.x, c.y - 1}
					if new.y < 1 {
						new.y = height - 1
					}
				default: // walls, and whatever else that doesn't move
					new = Coordinate{c.x, c.y}
				}
				if _, ok := blizzards[i][new]; ok {
					// already have a blizzard at that coordinate, add this one
					blizzards[i][new] = append(blizzards[i][new], b)
				} else {
					// create new list of blizzards at that coordinate
					blizzards[i][new] = []string{b}
				}
			}
		}
	}
	return blizzards, height, width
}

// encode a location in space together with the time
type Location struct {
	pos  Coordinate
	time int
}

// search the best path through the valley
func Search(start Location, goal Coordinate, bs Blizzards, h, w int) int {
	// basic BFS, with the addition of also tracking the time each node is explored
	// keep track of locations that have already been explored
	visited := make(map[Location]struct{})
	visited[start] = struct{}{}
	q := make([]Location, 1)
	q[0] = start
	for len(q) > 0 {
		c := q[0]
		q = q[1:]
		// try all four directions
		for _, o := range []Coordinate{{1, 0}, {0, 1}, {-1, 0}, {0, -1}} {
			n := Location{pos: Coordinate{c.pos.x + o.x, c.pos.y + o.y}, time: c.time + 1}
			if n.pos.x == goal.x && n.pos.y == goal.y {
				// go to the goal, done
				return n.time
			}
			if n.pos.x < 1 || n.pos.x >= w || n.pos.y < 1 || n.pos.y >= h {
				// out of bounds, as the top/bottom row and left/right col are walls
				continue
			}
			if _, seen := visited[n]; seen {
				// already explored, skip the candidate
				continue
			}
			if _, blocked := bs[n.time%len(bs)][Coordinate{n.pos.x, n.pos.y}]; !blocked {
				// the candidate location is not blocked by a blizzard next turn
				// append it to locations to explore
				visited[n] = struct{}{}
				q = append(q, n)
			}
		}
		if _, blocked := bs[(c.time+1)%len(bs)][c.pos]; !blocked {
			// staying put is an option as long as the current location won't be
			// blocked by a blizzard next turn
			q = append(q, Location{pos: c.pos, time: c.time + 1})
		}
	}
	return math.MaxInt32
}

func main() {
	blizzards, height, width := ReadInput(os.Args[1])
	start := Location{pos: Coordinate{1, 0}, time: 0}
	// goal is (6, 5) for the test input
	goal := Coordinate{120, 26}

	timePart1 := Search(start, goal, blizzards, height, width)
	fmt.Printf("Solution 1: %d\n", timePart1)

	start = Location{pos: goal, time: timePart1}
	goal = Coordinate{1, 0}
	timePart2a := Search(start, goal, blizzards, height, width)
	start = Location{pos: Coordinate{1, 0}, time: timePart2a}
	goal = Coordinate{120, 26}
	timePart2b := Search(start, goal, blizzards, height, width)
	fmt.Printf("Solution 2: %d\n", timePart2b)
}
