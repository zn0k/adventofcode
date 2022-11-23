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

type Floorplan map[Point]int64

type Robot struct {
	position Point
}

func (r *Robot) Move(direction int64, in chan int64, out chan int64) int64 {
	in <- direction
	result := <-out
	if result != WALL {
		switch direction {
		case NORTH:
			r.position.y++
		case SOUTH:
			r.position.y--
		case WEST:
			r.position.x--
		case EAST:
			r.position.x++
		}
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

	floorplan := make(Floorplan)
	robot := Robot{Point{0, 0}}

	go ic.Run()

	for {

	}
}
