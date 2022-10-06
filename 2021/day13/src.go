package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Coordinate struct {
	x, y int
}

type World [][]bool

type Fold struct {
	axis  string
	index int
}

func calculateDimensions(cs []Coordinate) (width, height int) {
	for _, c := range cs {
		if c.x > width {
			width = c.x
		}
		if c.y > height {
			height = c.y
		}
	}
	return
}

func parseCoordinates(s string) Coordinate {
	fields := strings.Split(s, ",")
	x, err := strconv.ParseInt(fields[0], 10, 32)
	if err != nil {
		panic(err)
	}
	y, err := strconv.ParseInt(fields[1], 10, 32)
	if err != nil {
		panic(err)
	}
	return Coordinate{int(x), int(y)}
}

func parseFold(s string) Fold {
	fields := strings.Fields(s)
	fields = strings.Split(fields[2], "=")
	pos, err := strconv.ParseInt(fields[1], 10, 32)
	if err != nil {
		panic(err)
	}
	return Fold{fields[0], int(pos)}
}

func readLines(p string) (World, []Fold, error) {
	f, err := os.Open(p)
	if err != nil {
		return nil, nil, err
	}

	var coordinates []Coordinate
	var folds []Fold
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := scanner.Text()
		if strings.Contains(line, ",") {
			coordinates = append(coordinates, parseCoordinates(line))
		} else if strings.Contains(line, "=") {
			folds = append(folds, parseFold(line))
		}
	}

	width, height := calculateDimensions(coordinates)
	var world World
	for y := 0; y < height+1; y++ {
		row := make([]bool, width+1)
		world = append(world, row)
	}
	for _, c := range coordinates {
		world[c.y][c.x] = true
	}

	return world, folds, scanner.Err()
}

func printWorld(w *World) {
	for _, row := range *w {
		for _, v := range row {
			if v {
				fmt.Print("#")
			} else {
				fmt.Print(".")
			}
		}
		fmt.Printf("\n")
	}
	fmt.Printf("\n")
}

func foldHorizontal(w *World, pos int) World {
	top := (*w)[0:pos]
	bottom := (*w)[pos+1:]
	for i, j := 0, len(bottom)-1; i < j; i, j = i+1, j-1 {
		bottom[i], bottom[j] = bottom[j], bottom[i]
	}
	for y := 0; y < len(bottom); y++ {
		for x := 0; x < len(bottom[y]); x++ {
			if bottom[y][x] {
				top[y][x] = true
			}
		}
	}
	return top
}

func foldVertical(w *World, pos int) World {
	var left World
	var right World
	for y := 0; y < len(*w); y++ {
		left = append(left, make([]bool, pos))
		right = append(right, make([]bool, pos))
		for x := 0; x < len((*w)[y]); x++ {
			if x < pos {
				left[y][x] = (*w)[y][x]
			} else if x > pos {
				transposed := len((*w)[y]) - x - 1
				right[y][transposed] = (*w)[y][x]
			}
		}
	}
	for y := 0; y < len(right); y++ {
		for x := 0; x < len(right[y]); x++ {
			if right[y][x] {
				left[y][x] = true
			}
		}
	}
	return left
}

func countPoints(w *World) (c int) {
	for _, row := range *w {
		for _, v := range row {
			if v {
				c++
			}
		}
	}
	return
}

func fold(w *World, f *Fold) World {
	if f.axis == "x" {
		return foldVertical(w, f.index)
	} else {
		return foldHorizontal(w, f.index)
	}
}

func main() {
	world, folds, err := readLines(os.Args[1])
	if err != nil {
		panic(err)
	}

	world = fold(&world, &folds[0])
	fmt.Printf("Solution 1: %d\n", countPoints(&world))

	for _, f := range folds[1:] {
		world = fold(&world, &f)
	}
	fmt.Printf("\nSolution 2:\n")
	printWorld(&world)
}
