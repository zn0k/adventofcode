package main

import (
	"fmt"
	"image"
	"image/png"
	"intcode"
	"io/ioutil"
	"os"
	"strings"
)

const (
	UP    = 0
	RIGHT = 1
	DOWN  = 2
	LEFT  = 3

	BLACK = 0
	WHITE = 1

	TURNLEFT  = 0
	TURNRIGHT = 1
)

type Point struct {
	x int64
	y int64
}

type Robot struct {
	Position  Point
	Direction int64
}

func (r *Robot) Turn(dir int64) {
	switch dir {
	case TURNLEFT:
		r.Direction--
	case TURNRIGHT:
		r.Direction++
	default:
		panic(fmt.Sprintf("Invalid turn direction %d", dir))
	}

	if r.Direction < UP {
		r.Direction = LEFT
	}
	if r.Direction > LEFT {
		r.Direction = UP
	}
}

func (r *Robot) Move() {
	switch r.Direction {
	case UP:
		r.Position.x--
	case RIGHT:
		r.Position.y++
	case DOWN:
		r.Position.x++
	case LEFT:
		r.Position.y--
	default:
		panic(fmt.Sprintf("Robot pointed at invalid direction %d", r.Direction))
	}
}

func runRobot(program string, startingColor int64) map[Point]int64 {
	in := make(chan int64, 2)
	out := make(chan int64, 2)

	ic := intcode.New(in, out)
	ic.Load(strings.NewReader(program))

	start := Point{x: 0, y: 0}
	points := make(map[Point]int64)
	points[start] = startingColor
	robot := Robot{Position: Point{x: 0, y: 0}, Direction: UP}

	in <- points[start]

	go ic.Run()

	for {
		color, ok := <-out
		if !ok {
			break
		}
		direction := <-out
		points[robot.Position] = color
		robot.Turn(direction)
		robot.Move()
		_, ok = points[robot.Position]
		if ok {
			in <- points[robot.Position]
		} else {
			in <- BLACK
		}
	}

	return points
}

func scale(pixels map[Point]int64) (map[Point]int64, int64, int64) {
	var minX int64 = 0
	var minY int64 = 0
	var maxX int64 = 0
	var maxY int64 = 0
	for point, _ := range pixels {
		if point.x < minX {
			minX = point.x
		}
		if point.y < minY {
			minY = point.y
		}
		if point.x > maxX {
			maxX = point.x
		}
		if point.y > maxY {
			maxY = point.y
		}
	}

	scaleX := 0 - minX
	scaleY := 0 - minY

	result := make(map[Point]int64)

	for point, color := range pixels {
		result[Point{x: point.x + scaleX, y: point.y + scaleY}] = color
	}
	return result, maxX + scaleX, maxY + scaleY
}

func getDimensions(pixels map[Point]int64) (image.Point, image.Point) {
	var minX int64 = 0
	var minY int64 = 0
	var maxX int64 = 0
	var maxY int64 = 0
	for point, _ := range pixels {
		if point.x < minX {
			minX = point.x
		}
		if point.y < minY {
			minY = point.y
		}
		if point.x > maxX {
			maxX = point.x
		}
		if point.y > maxY {
			maxY = point.y
		}
	}

	return image.Point{int(minY), int(minX)}, image.Point{int(maxY) + 10, int(maxX) + 10}
}

func main() {
	buf, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic("Unable to open input.txt for reading")
	}
	program := string(buf)

	solution1 := runRobot(program, BLACK)
	fmt.Printf("Solution 1: %d\n", len(solution1))

	solution2 := runRobot(program, WHITE)
	width, height := getDimensions(solution2)
	img := image.NewRGBA(image.Rectangle{width, height})
	for pixel, color := range solution2 {
		if color == WHITE {
			img.Set(int(pixel.y), int(pixel.x), image.White)
		}
	}

	f, _ := os.Create("day11.png")
	png.Encode(f, img)
	fmt.Println("Wrote solution 2 to day11.png")
}
