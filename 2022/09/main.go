package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Coordinate struct {
	X, Y int
}

func (c *Coordinate) Touches(o Coordinate) bool { return Abs(c.X-o.X) <= 1 && Abs(c.Y-o.Y) <= 1 }

func (c *Coordinate) IsLeft(o Coordinate) bool  { return c.X < o.X }
func (c *Coordinate) IsRight(o Coordinate) bool { return c.X > o.X }
func (c *Coordinate) IsUp(o Coordinate) bool    { return c.Y > o.Y }
func (c *Coordinate) IsDown(o Coordinate) bool  { return c.Y < o.Y }

func (c *Coordinate) SameRow(o Coordinate) bool { return c.Y == o.Y }
func (c *Coordinate) SameCol(o Coordinate) bool { return c.X == o.X }

func (c *Coordinate) Move(dir Coordinate) { c.X, c.Y = c.X+dir.X, c.Y+dir.Y }
func (c *Coordinate) MoveRight()          { c.Move(Coordinate{X: 1, Y: 0}) }
func (c *Coordinate) MoveLeft()           { c.Move(Coordinate{X: -1, Y: 0}) }
func (c *Coordinate) MoveUp()             { c.Move(Coordinate{X: 0, Y: 1}) }
func (c *Coordinate) MoveDown()           { c.Move(Coordinate{X: 0, Y: -1}) }

type Move struct {
	Direction Coordinate
	Times     int
}

type Rope struct {
	// the knots are in a list, with the last element being the head
	// and the first element being the tail
	Knots []Coordinate
	// also track the index of the head in the above
	Head int
	// track coordinates the tail has seen
	Visited map[Coordinate]bool
}

func (r *Rope) Move(m Move) {
	// repeat the move as often as needed
	for i := 0; i < m.Times; i += 1 {
		// move the head
		r.Knots[r.Head].Move(m.Direction)
		// move down the list of knots and have each follow its predecessor
		for j := r.Head; j >= 1; j -= 1 {
			if !r.Knots[j].Touches(r.Knots[j-1]) {
				if r.Knots[j].IsRight(r.Knots[j-1]) {
					r.Knots[j-1].MoveRight()
				}
				if r.Knots[j].IsLeft(r.Knots[j-1]) {
					r.Knots[j-1].MoveLeft()
				}
				if r.Knots[j].IsUp(r.Knots[j-1]) {
					r.Knots[j-1].MoveUp()
				}
				if r.Knots[j].IsDown(r.Knots[j-1]) {
					r.Knots[j-1].MoveDown()
				}
			}
		}
		// record the tail location
		r.Visited[r.Knots[0]] = true
	}
}

func (r *Rope) Count() int {
	return len(r.Visited)
}

func NewRope(knots int) *Rope {
	if knots < 2 {
		panic(fmt.Sprintf("rope must have at least 2 knots, got %d", knots))
	}
	r := &Rope{Head: knots - 1}
	r.Knots = make([]Coordinate, knots)
	for i := 0; i < knots; i += 1 {
		r.Knots[i] = Coordinate{X: 0, Y: 0}
	}
	r.Visited = make(map[Coordinate]bool)
	r.Visited[Coordinate{X: 0, Y: 0}] = true
	return r
}

// absolute value of integers, builtin only works on floats
func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func ReadInput(path string) []Move {
	f, err := os.Open(path)
	if err != nil {
		panic(fmt.Sprintf("unable to open %s for reading", path))
	}
	defer f.Close()

	var moves []Move

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		fields := strings.Fields(scanner.Text())
		times, _ := strconv.Atoi(fields[1])
		switch fields[0] {
		case "U":
			moves = append(moves, Move{Direction: Coordinate{X: 0, Y: 1}, Times: times})
		case "D":
			moves = append(moves, Move{Direction: Coordinate{X: 0, Y: -1}, Times: times})
		case "L":
			moves = append(moves, Move{Direction: Coordinate{X: -1, Y: 0}, Times: times})
		case "R":
			moves = append(moves, Move{Direction: Coordinate{X: 1, Y: 0}, Times: times})
		}
	}

	return moves
}

func main() {
	moves := ReadInput(os.Args[1])
	rope := NewRope(2)
	for _, move := range moves {
		rope.Move(move)
	}
	fmt.Printf("Solution 1: %d\n", rope.Count())

	rope = NewRope(10)
	for _, move := range moves {
		rope.Move(move)
	}
	fmt.Printf("Solution 2: %d\n", rope.Count())
}
