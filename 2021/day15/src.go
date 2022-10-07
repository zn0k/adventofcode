package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"

	"gonum.org/v1/gonum/graph/path"
	"gonum.org/v1/gonum/graph/simple"
	"gonum.org/v1/gonum/mat"
)

type Coordinate struct {
	x, y int
}

func (c *Coordinate) Uid(width int) int64 {
	y := int64(c.y)
	x := int64(c.x)
	return y*int64(width) + x
}

func readLines(p string) *mat.Dense {
	file, err := os.Open(p)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	var lines []string

	for scanner.Scan() {
		line := scanner.Text()
		lines = append(lines, line)
	}

	height, width := len(lines), len(lines[0])
	var values []float64

	for _, row := range lines {
		for _, r := range row {
			n, err := strconv.ParseFloat(string(r), 64)
			if err != nil {
				panic(err)
			}
			values = append(values, n)
		}
	}
	world := mat.NewDense(height, width, values)
	return world
}

func getNeighbors(c *Coordinate, w *mat.Dense) (ns []Coordinate) {
	height, width := w.Dims()
	offsets := []Coordinate{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}

	for _, o := range offsets {
		n := Coordinate{c.x + o.x, c.y + o.y}
		if n.x >= 0 && n.x < width && n.y >= 0 && n.y < height {
			ns = append(ns, n)
		}
	}
	return
}

func getCost(w *mat.Dense) float64 {
	height, width := w.Dims()
	g := simple.NewWeightedDirectedGraph(0, math.Inf(1))
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			c := Coordinate{x, y}
			for _, n := range getNeighbors(&c, w) {
				e := simple.WeightedEdge{
					F: simple.Node(c.Uid(width)),
					T: simple.Node(n.Uid(width)),
					W: w.At(n.y, n.x),
				}
				g.SetWeightedEdge(e)
			}
		}
	}
	from, to := Coordinate{0, 0}, Coordinate{width - 1, height - 1}
	shortest := path.DijkstraFrom(simple.Node(from.Uid(width)), g)
	_, weight := shortest.To(to.Uid(width))
	return weight
}

func increasePointValue(y, x int, v float64) float64 {
	v++
	if v > 9 {
		v = 1
	}
	return v
}

func printWorld(w *mat.Dense) {
	height, _ := w.Dims()
	for i := 0; i < height; i++ {
		strs := []string{}
		for _, v := range w.RawRowView(i) {
			strs = append(strs, strconv.FormatFloat(v, 'f', 0, 64))
		}
		fmt.Print(strings.Join(strs, "") + "\n")
	}
}

func growWorld(w *mat.Dense) *mat.Dense {
	height, width := w.Dims()
	var combined *mat.Dense
	tile := mat.NewDense(height, width, nil)
	tile.Copy(w)
	for i := 0; i < 4; i++ {
		tile.Apply(increasePointValue, tile)
		_, worldWidth := w.Dims()
		combined = mat.NewDense(height, worldWidth+width, nil)
		combined.Augment(w, tile)
		w = combined
	}
	height, width = w.Dims()
	tile = mat.NewDense(height, width, nil)
	tile.Copy(w)
	for i := 0; i < 4; i++ {
		tile.Apply(increasePointValue, tile)
		worldHeight, _ := w.Dims()
		combined = mat.NewDense(worldHeight+height, width, nil)
		combined.Stack(w, tile)
		w = combined
	}
	return w
}

func main() {
	world := readLines(os.Args[1])
	fmt.Printf("Solution 1: %v\n", getCost(world))
	world = growWorld(world)
	fmt.Printf("Solution 2: %v\n", getCost(world))
}
