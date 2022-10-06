package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"

	"gonum.org/v1/gonum/graph/path"
	"gonum.org/v1/gonum/graph/simple"
)

type World [][]int

type Coordinate struct {
	x, y int
}

func (c *Coordinate) Uid(width int) int64 {
	y := int64(c.y)
	x := int64(c.x)
	return y*int64(width+1) + x
}

func getDimensions(w *World) (width, height int) {
	height = len(*w) - 1
	width = len((*w)[0]) - 1
	return
}

func readLines(p string) (World, error) {
	file, err := os.Open(p)
	if err != nil {
		return nil, err
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)

	var world World

	for scanner.Scan() {
		line := scanner.Text()
		row := make([]int, len(line))
		for i, r := range line {
			n, err := strconv.ParseInt(string(r), 10, 32)
			if err != nil {
				return nil, err
			}
			row[i] = int(n)
		}
		world = append(world, row)
	}
	return world, scanner.Err()
}

func getNeighbors(c *Coordinate, w *World) (ns []Coordinate) {
	offsets := []Coordinate{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	width, height := getDimensions(w)

	for _, o := range offsets {
		n := Coordinate{c.x + o.x, c.y + o.y}
		if n.x >= 0 && n.x <= width && n.y >= 0 && n.y <= height {
			ns = append(ns, n)
		}
	}
	return
}

func getCost(w *World) float64 {
	width, height := getDimensions(w)
	g := simple.NewWeightedDirectedGraph(0, math.Inf(1))
	for y := 0; y <= height; y++ {
		for x := 0; x <= width; x++ {
			c := Coordinate{x, y}
			for _, n := range getNeighbors(&c, w) {
				e := simple.WeightedEdge{
					F: simple.Node(c.Uid(width)),
					T: simple.Node(n.Uid(width)),
					W: float64((*w)[n.y][n.x]),
				}
				g.SetWeightedEdge(e)
			}
		}
	}
	from, to := Coordinate{0, 0}, Coordinate{width, height}
	shortest := path.DijkstraFrom(simple.Node(from.Uid(width)), g)
	_, weight := shortest.To(to.Uid(width))
	return weight
}

func increaseWorld(w *World) World {
	width, height := getDimensions(w)
	new := make(World, height+1)
	for y := 0; y < height; y++ {
		row := make([]int, width+1)
		new[y] = row
		for x := 0; x < width; x++ {
			n := (*w)[y][x] + 1
			if n > 9 {
				new[y][x] = 1
			} else {
				new[y][x] = n
			}
		}
	}
	return new
}

func expandWorld(w *World) World {
	width, height := getDimensions(w)
	var new World
	return new
}

func main() {
	world, err := readLines(os.Args[1])
	if err != nil {
		panic(err)
	}

	fmt.Printf("Solution 1: %v\n", getCost(&world))

}
