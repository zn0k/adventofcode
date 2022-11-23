package main

import (
	"intcode"
	"io/ioutil"
	"strings"
)

const (
	NORTH = 1
	SOUTH = 2
	WEST  = 3
	EAST  = 4

	WALL   = 0
	EMPTY  = 1
	OXYGEN = 2
)

type Point struct {
	x, y int64
}

type Floorplan map[int64]map[int64]int64

type Robot struct {
	position  Point
	floorplan Floorplan
}

func NewRobot() *Robot {
	r := &Robot{position: Point{0, 0}}
	r.floorplan = make(Floorplan)
	return r
}

func (r *Robot) Move(direction int64, in chan int64, out chan int64) int64 {
	proposed_position := Point{r.position.x, r.position.y}
	switch direction {
	case NORTH:
		proposed_position.y++
	case SOUTH:
		proposed_position.y--
	case EAST:
		proposed_position.x++
	case WEST:
		proposed_position.x--
	}

	in <- direction
	result := <-out
	r.floorplan[proposed_position.x][proposed_position.y] = result

	if result != WALL {
		r.position = proposed_position
	}
	return result
}

func main() {
	buf, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic("Unable to open input.txt for reading")
	}
	program := string(buf)

	in := make(chan int64, 2)
	out := make(chan int64, 2)

	ic := intcode.New(in, out)
	ic.Load(strings.NewReader(program))

	robot := NewRobot()

	go ic.Run()

	for {

	}
}
