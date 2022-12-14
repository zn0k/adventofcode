package main

import (
	"fmt"
	"image"
	"image/color"
	"image/png"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

type Coordinate struct{ X, Y int }

func (c *Coordinate) Add(o Coordinate) Coordinate { return Coordinate{c.X + o.X, c.Y + o.Y} }
func (c *Coordinate) Move(o Coordinate) {
	c.X += o.X
	c.Y += o.Y
}

func NewCoordinate(in string) *Coordinate {
	fields := strings.Split(in, ",")
	x, _ := strconv.Atoi(fields[0])
	y, _ := strconv.Atoi(fields[1])
	return &Coordinate{x, y}
}

type Line struct {
	Start, End Coordinate
}

var down Coordinate = Coordinate{0, 1}
var left Coordinate = Coordinate{-1, 1}
var right Coordinate = Coordinate{1, 1}

const (
	AIR = iota
	SOURCE
	ROCK
	SAND
)

type World struct {
	Grid                [][]int
	Width, Height, Sand int
}

func NewWorld(width, height int) *World {
	w := &World{Width: width, Height: height}
	w.Grid = make([][]int, height)
	for i := 0; i < height; i += 1 {
		row := make([]int, width)
		w.Grid[i] = row
	}
	w.Grid[0][500] = SOURCE
	return w
}

func (w *World) Set(c Coordinate, material int) { w.Grid[c.Y][c.X] = material }
func (w *World) Get(c Coordinate) int           { return w.Grid[c.Y][c.X] }

func (w *World) DrawRock(start, end Coordinate) {
	if start.X > end.X || start.Y > end.Y {
		start, end = end, start
	}
	for y := start.Y; y <= end.Y; y += 1 {
		for x := start.X; x <= end.X; x += 1 {
			w.Grid[y][x] = ROCK
		}
	}
}

func (w *World) Fill() {
	done := false
	for !done {
		sand, settled := Coordinate{500, 0}, false
		for !settled {
			if sand.Y >= w.Height-1 { // sand has slid off the edge of the world
				done = true
				break
			}
			if w.Get(sand.Add(down)) == AIR {
				sand.Move(down)
			} else if w.Get(sand.Add(left)) == AIR {
				sand.Move(left)
			} else if w.Get(sand.Add(right)) == AIR {
				sand.Move(right)
			} else {
				settled = true
				if w.Get(sand) == SOURCE { // sand has piled up to source
					done = true
				}
				w.Set(sand, SAND) // settle the sand at its final location
				w.Sand += 1
			}
		}
	}
}

func (w *World) ClearSand() {
	for y := 0; y < len(w.Grid); y += 1 {
		for x := 0; x < len(w.Grid[0]); x += 1 {
			if w.Grid[y][x] == SAND {
				w.Grid[y][x] = AIR
			}
		}
	}
}

func (w *World) AsImage(path string) {
	width, height := image.Point{0, 0}, image.Point{w.Width, w.Height}
	img := image.NewRGBA(image.Rectangle{width, height})
	black := color.RGBA{0x00, 0x00, 0x00, 0xff}
	blue := color.RGBA{0x00, 0x00, 0xff, 0xff}
	yellow := color.RGBA{0xff, 0xff, 0x00, 0xff}
	gray := color.RGBA{0xa9, 0xa9, 0xa9, 0xff}
	for y := 0; y < len(w.Grid); y += 1 {
		for x := 0; x < len(w.Grid[0]); x += 1 {
			color := black
			switch w.Grid[y][x] {
			case SOURCE:
				color = blue
			case ROCK:
				color = gray
			case SAND:
				color = yellow
			}
			img.Set(x, y, color)
		}
	}
	f, _ := os.Create(path)
	png.Encode(f, img)
}

func ReadLines(path string) (*World, int) {
	buf, err := ioutil.ReadFile(path)
	if err != nil {
		panic(fmt.Sprintf("unable to open %s for reading", path))
	}

	width, height := 0, 0
	var lines []Line
	for _, line := range strings.Split(string(buf), "\n") {
		coordinates := strings.Split(line, " -> ")
		for i := 0; i < len(coordinates)-1; i += 1 {
			start := NewCoordinate(coordinates[i])
			end := NewCoordinate(coordinates[i+1])
			if end.X > width {
				width = end.X
			}
			if end.Y > height {
				height = end.Y
			}
			lines = append(lines, Line{*start, *end})
		}
	}

	world := NewWorld(width*2, height+3)
	for _, line := range lines {
		world.DrawRock(line.Start, line.End)
	}

	return world, height
}

func main() {
	world, max_height := ReadLines(os.Args[1])
	world.Fill()
	fmt.Printf("Solution 1: %d\n", world.Sand)
	world.AsImage("day14-1.png")

	world.ClearSand()
	line := Line{Coordinate{0, max_height + 2}, Coordinate{world.Width - 1, max_height + 2}}
	world.DrawRock(line.Start, line.End)
	world.Fill()
	fmt.Printf("Solution 2: %d\n", world.Sand)
	world.AsImage("day14-2.png")
}
