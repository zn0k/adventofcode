package main

import (
	"fmt"
	"intcode"
	"io/ioutil"
	"strings"
)

const (
	EMPTY  = 0
	WALL   = 1
	BLOCK  = 2
	PADDLE = 3
	BALL   = 4
)

type Tile struct {
	kind int64
}

type Point struct {
	x, y int64
}

func main() {
	buf, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic("Unable to open input.txt for reading")
	}
	program := string(buf)

	tiles := make(map[Point]Tile)

	in := make(chan int64, 2)
	out := make(chan int64, 2)

	ic := intcode.New(in, out)
	ic.Load(strings.NewReader(program))

	go ic.Run()

	for {
		// try to read in another triplet of values
		// if the first one fails, the channel is closed and the program halted
		x, ok := <-out
		if !ok {
			break
		}
		// read the remaining two values
		y := <-out
		id := <-out
		// remember that a tile of that type was drawn at that point
		tiles[Point{x, y}] = Tile{id}
	}

	// count the block type tiles
	var blocks int = 0
	for _, t := range tiles {
		if t.kind == BLOCK {
			blocks++
		}
	}

	fmt.Printf("Solution 1: %d\n", blocks)

	in = make(chan int64, 2)
	out = make(chan int64, 2)
	ic = intcode.New(in, out)
	ic.Load(strings.NewReader(program))
	ic.Write(0, 2) // put in two quarters

	var joystick int64 = 0
	var score int64
	var ballPosition Point = Point{-1, -1}
	var paddlePosition Point = Point{-1, -1}

	go ic.Run()

	for {
		// run it all again
		x, ok := <-out
		if !ok {
			break
		}
		y := <-out
		id := <-out

		if x == -1 && y == 0 {
			// remember the score whenever it is updated
			score = id
		}

		if id == PADDLE {
			// if a paddle is being drawn, remember where it is
			paddlePosition = Point{x, y}
		}
		if id == BALL {
			// if a ball is being drawn, remember where it is
			ballPosition = Point{x, y}
			// check if we know where both the ball and the paddle are
			if paddlePosition.x >= 0 && ballPosition.x >= 0 {
				// if the paddle is to the left of the ball...
				if paddlePosition.x < ballPosition.x {
					// ... tile the joystick right
					joystick = 1
				} else if paddlePosition.x > ballPosition.x {
					// if it's to the right, tilt it left
					joystick = -1
				} else {
					// they're aligned, leave it where it is
					joystick = 0
				}
			}
			// and pass on the joystick signal
			in <- joystick
		}
	}

	fmt.Printf("Solution 2: %d\n", score)
}
