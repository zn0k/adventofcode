package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"strings"
)

const (
	_ = iota
	NORTH
	SOUTH
	WEST
	EAST
)

type Coordinate struct {
	x, y int
}

func (c *Coordinate) Add(o Coordinate) Coordinate { return Coordinate{c.x + o.x, c.y + o.y} }
func (c *Coordinate) N() Coordinate               { return Coordinate{c.x, c.y - 1} }
func (c *Coordinate) NE() Coordinate              { return Coordinate{c.x + 1, c.y - 1} }
func (c *Coordinate) E() Coordinate               { return Coordinate{c.x + 1, c.y} }
func (c *Coordinate) SE() Coordinate              { return Coordinate{c.x + 1, c.y + 1} }
func (c *Coordinate) S() Coordinate               { return Coordinate{c.x, c.y + 1} }
func (c *Coordinate) SW() Coordinate              { return Coordinate{c.x - 1, c.y + 1} }
func (c *Coordinate) W() Coordinate               { return Coordinate{c.x - 1, c.y} }
func (c *Coordinate) NW() Coordinate              { return Coordinate{c.x - 1, c.y - 1} }
func (c *Coordinate) Neighbors() []Coordinate {
	ns := make([]Coordinate, 8)
	offsets := []Coordinate{{1, 0}, {1, -1}, {0, -1}, {-1, -1}, {-1, 0}, {-1, 1}, {0, 1}, {1, 1}}
	for i := 0; i < len(offsets); i += 1 {
		ns[i] = c.Add(offsets[i])
	}
	return ns
}

func (c *Coordinate) Move(dir int) Coordinate {
	switch dir {
	case NORTH:
		return c.N()
	case SOUTH:
		return c.S()
	case WEST:
		return c.W()
	case EAST:
		return c.E()
	default:
		return c.Add(Coordinate{0, 0})
	}
}

type Elves struct {
	m     map[Coordinate]struct{}
	order []int
}

func NewElves() Elves {
	e := Elves{}
	e.m = make(map[Coordinate]struct{})
	e.order = []int{NORTH, SOUTH, WEST, EAST}
	return e
}

func (e *Elves) Add(c Coordinate)    { e.m[c] = struct{}{} }
func (e *Elves) Remove(c Coordinate) { delete(e.m, c) }
func (e *Elves) ShuffleOrder()       { e.order = append(e.order[1:], e.order[0]) }

func (e *Elves) Positions() []Coordinate {
	var cs []Coordinate
	for key := range e.m {
		cs = append(cs, key)
	}
	return cs
}

func (e *Elves) At(c Coordinate) bool {
	_, ok := e.m[c]
	return ok
}

func (e *Elves) HasNeighbors(c Coordinate) bool {
	result := false
	for _, n := range c.Neighbors() {
		result = result || e.At(n)
	}
	return result
}

func (e *Elves) HasDirectionalNeighbors(c Coordinate, dir int) bool {
	switch dir {
	case NORTH:
		if e.At(c.NW()) || e.At(c.N()) || e.At(c.NE()) {
			return true
		}
	case SOUTH:
		if e.At(c.SW()) || e.At(c.S()) || e.At(c.SE()) {
			return true
		}
	case WEST:
		if e.At(c.NW()) || e.At(c.W()) || e.At(c.SW()) {
			return true
		}
	case EAST:
		if e.At(c.NE()) || e.At(c.E()) || e.At(c.SE()) {
			return true
		}
	}
	return false
}

func (e *Elves) Directions() []int { return e.order }

func (e *Elves) Score() int {
	minX, minY, maxX, maxY := math.MaxInt32, math.MaxInt32, math.MinInt32, math.MinInt32
	for e := range e.m {
		if e.x < minX {
			minX = e.x
		}
		if e.x > maxX {
			maxX = e.x
		}
		if e.y < minY {
			minY = e.y
		}
		if e.y > maxY {
			maxY = e.y
		}
	}
	return (maxX-minX+1)*(maxY-minY+1) - len(e.m)
}

func ReadInput(path string) Elves {
	buf, _ := ioutil.ReadFile(path)
	lines := strings.Split(string(buf), "\n")

	elves := NewElves()
	for y := 0; y < len(lines); y += 1 {
		chars := strings.Split(lines[y], "")
		for x := 0; x < len(chars); x += 1 {
			if chars[x] == "#" {
				elves.Add(Coordinate{x, y})
			}
		}
	}
	return elves
}

func main() {
	elves := ReadInput(os.Args[1])
	rounds := 1
	for {
		fromTo := make(map[Coordinate]Coordinate) // map current elf coordinate to proposed one
		toFrom := make(map[Coordinate]Coordinate) // map proposed elf coordinate to current one
		blocked := make(map[Coordinate]struct{})  // keep track of coordinates that no elf can move to

		for _, elf := range elves.Positions() { // go through all elves
			if !elves.HasNeighbors(elf) { // no neighbors at all  for this elf, stay put
				continue
			}
			for _, dir := range elves.Directions() { // try the four directions one by one
				if !elves.HasDirectionalNeighbors(elf, dir) {
					// elf has no neighbors in the proposed direction, calculate the new coordinate
					proposed := elf.Move(dir)
					// check if previous collisions rule out that location
					if _, collision := blocked[proposed]; collision {
						break
					}
					// check if someone else has already proposed to move there
					if otherElf, collision := toFrom[proposed]; collision {
						// yes, someone else wants to go there. undo their move
						delete(fromTo, otherElf)
						delete(toFrom, proposed)
						// mark that coordinate as blocked
						blocked[proposed] = struct{}{}
						break
					}
					// record the proposed move
					fromTo[elf] = proposed
					toFrom[proposed] = elf
					// no need to try other directions
					break
				}
			}
		}
		if rounds == (10 + 1) {
			fmt.Printf("Solution 1: %d\n", elves.Score())
		}
		// check if any elves are moving
		if len(toFrom) == 0 {
			break
		}

		// toFrom now contains all legal moves. go through it and move all those elves
		for to, from := range toFrom {
			elves.Remove(from)
			elves.Add(to)
		}
		// shuffle the order of directions checked and increase the round counter
		elves.ShuffleOrder()
		rounds += 1
	}

	fmt.Printf("Solution 2: %d\n", rounds)
}
