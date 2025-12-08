package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"

	"gonum.org/v1/gonum/graph/simple"
	"gonum.org/v1/gonum/graph/topo"
)

type Coordinate struct {
	X, Y, Z int
}

type CoordinatePair struct {
	A, B     Coordinate
	Distance float64
}

// euclidean distance between two coordinates
func dist(a, b Coordinate) float64 {
	dx := b.X - a.X
	dy := b.Y - a.Y
	dz := b.Z - a.Z
	return math.Sqrt(float64(dx*dx + dy*dy + dz*dz))
}

// turn input file into a list of coordinates
func readInput(fname string) []Coordinate {
	file, _ := os.Open(fname)

	defer file.Close()

	var coordinates []Coordinate

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		// pull out the number components separated by commas
		components := strings.Split(scanner.Text(), ",")
		// convert to integers
		nums := make([]int, 3)
		for i := 0; i < 3; i++ {
			nums[i], _ = strconv.Atoi(components[i])
		}
		// and cast to coordinate type
		coordinates = append(coordinates, Coordinate{nums[0], nums[1], nums[2]})
	}

	return coordinates
}

// create all pairs of coordinates, sorted by the distance within each pair
func combinationsByDistance(coordinates []Coordinate) []CoordinatePair {
	pairs := make([]CoordinatePair, 0)

	// walk the coordinates and create the pairs
	for i := 0; i < len(coordinates); i++ {
		for j := i + 1; j < len(coordinates); j++ {
			pairs = append(pairs, CoordinatePair{
				coordinates[i],
				coordinates[j],
				dist(coordinates[i], coordinates[j]),
			})
		}
	}

	// sort by distance, ascending
	sort.Slice(pairs, func(i, j int) bool {
		return pairs[i].Distance < pairs[j].Distance
	})

	return pairs
}

// generate an int64 ID for a coordinate based on its components
func node_id(c Coordinate) int64 {
	return int64(c.X * c.Y * c.Z)
}

// solve part 1
func part1(pairs []CoordinatePair, n int) int {
	// create a graph
	g := simple.NewUndirectedGraph()

	// for as many steps as indicated, add nodes
	// and edges between them
	for i := 0; i < n; i++ {
		a_id := node_id(pairs[i].A)
		b_id := node_id(pairs[i].B)
		// need to check if a node is already present
		// before adding it
		if g.Node(a_id) == nil {
			g.AddNode(simple.Node(a_id))
		}
		if g.Node(b_id) == nil {
			g.AddNode(simple.Node(b_id))
		}
		g.SetEdge(simple.Edge{F: simple.Node(a_id), T: simple.Node(b_id)})
	}

	// fetch the components within the graph
	components := topo.ConnectedComponents(g)
	// get their lengths
	lengths := make([]int, len(components))
	for i := 0; i < len(components); i++ {
		lengths[i] = len(components[i])
	}
	// sort descending
	sort.Slice(lengths, func(i, j int) bool {
		return lengths[i] > lengths[j]
	})

	// multiply the size of the three largest ones
	return lengths[0] * lengths[1] * lengths[2]
}

// solve part 2
func part2(pairs []CoordinatePair) int64 {
	// create a graph
	g := simple.NewUndirectedGraph()

	// get all the unique IDs for all coordinates
	ids := make(map[int64]bool)
	for _, pair := range pairs {
		ids[node_id(pair.A)] = true
		ids[node_id(pair.B)] = true
	}

	// add them all to the graph
	for id := range ids {
		g.AddNode(simple.Node(id))
	}

	i := 0
	var last CoordinatePair
	n := len(topo.ConnectedComponents(g))
	// is the graph not yet fully connnected?
	// check by seeing if there's more than one component
	for n > 1 {
		// add the shortest remaining edge
		a_id := node_id(pairs[i].A)
		b_id := node_id(pairs[i].B)
		g.SetEdge(simple.Edge{F: simple.Node(a_id), T: simple.Node(b_id)})
		// keep track of the last pair to be connected by an edge
		last = pairs[i]
		n = len(topo.ConnectedComponents(g))
		i++
	}

	// multiply the last pair's X coordinates
	return int64(last.A.X) * int64(last.B.X)
}

// and run
func main() {
	coordinates := readInput("input.txt")
	pairs := combinationsByDistance(coordinates)
	solution1 := part1(pairs, 1000)
	solution2 := part2(pairs)
	fmt.Printf("Solution 1: %d\nSolution 2: %d\n", solution1, solution2)
}
