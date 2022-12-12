package main

import (
	"container/heap"
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"strings"
)

// pq shamelessly taken from https://pkg.go.dev/container/heap
// after all, that's _basically_ part of the std library

type Item struct {
	value    int
	priority int
	index    int
}

type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	// usually we'd do > here to get the max priority item
	// in this case we actually want the minimum weight next path
	return pq[i].priority < pq[j].priority
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *PriorityQueue) Push(x any) {
	n := len(*pq)
	item := x.(*Item)
	item.index = n
	*pq = append(*pq, item)
}

func (pq *PriorityQueue) Pop() any {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil
	item.index = -1
	*pq = old[0 : n-1]
	return item
}

// an adjacency is the neighbor the given node is adjacent to,
// and the weight to get there
type Adjacency struct {
	neighbor int
	weight   int
}

// each node will have a unique number increasing monotonically from zero
// the adjacency list uses that as an index to track all adjacencies a node has
type AdjacencyList [][]Adjacency

// return an adjacency list,  the index of the start node and the goal node,
// and the list of all lowest points
func ReadInput(path string) (AdjacencyList, int, int, []int) {
	buf, err := ioutil.ReadFile(path)
	if err != nil {
		panic(fmt.Sprintf("unable to open %s for reading", path))
	}

	// create a grid out of the input, with each character mapped to its int equivalent
	var grid [][]int
	for _, line := range strings.Split(string(buf), "\n") {
		var row []int
		for _, c := range line {
			row = append(row, int(c))
		}
		grid = append(grid, row)
	}

	height := len(grid)
	width := len(grid[0])

	// helper function to take an (x, y) grid coordinate and return the
	// list of valid adjacent node indices
	getNeighbors := func(x, y int) []Adjacency {
		var result []Adjacency

		current := grid[y][x]
		for _, direction := range []struct{ x, y int }{{0, 1}, {0, -1}, {1, 0}, {-1, 0}} {
			new_x, new_y := x+direction.x, y+direction.y
			if new_x < 0 || new_x >= width || new_y < 0 || new_y >= height {
				continue
			}
			if (grid[new_y][new_x] - 1) <= current {
				adj := Adjacency{neighbor: new_y*width + new_x, weight: 1}
				result = append(result, adj)
			}
		}
		return result
	}

	var start, end int
	var alternatives []int

	for y := 0; y < height; y += 1 {
		for x := 0; x < width; x += 1 {
			if rune(grid[y][x]) == 'S' {
				start = y*width + x
				grid[y][x] = int('a')
			} else if rune(grid[y][x]) == 'E' {
				end = y*width + x
				grid[y][x] = int('z')
			}
		}
	}

	adjs := make(AdjacencyList, width*height)

	// march through grid and find all adjacencies, also record start and goal node
	for y := 0; y < height; y += 1 {
		for x := 0; x < width; x += 1 {
			if rune(grid[y][x]) == 'a' {
				alternatives = append(alternatives, y*width+x)
			}
			adjs[y*width+x] = getNeighbors(x, y)
		}
	}
	return adjs, start, end, alternatives
}

// calculate the distance from node x to all other nodes given an adjacency list
func Dijkstra(xs []int, adjs AdjacencyList) map[int]int {
	distances := make(map[int]int)
	for i := 0; i < len(adjs); i += 1 {
		distances[i] = math.MaxInt32
	}
	for _, x := range xs {
		distances[x] = 0
	}

	visited := make(map[int]bool)

	q := make(PriorityQueue, len(xs))
	for i := 0; i < len(xs); i += 1 {
		q[i] = &Item{value: xs[i], priority: 0, index: i}
	}
	heap.Init(&q)

	for q.Len() > 0 {
		item := heap.Pop(&q).(*Item)
		_, done := visited[item.value]
		if done {
			continue
		}
		visited[item.value] = true

		for _, adj := range adjs[item.value] {
			if distances[item.value]+adj.weight < distances[adj.neighbor] {
				distances[adj.neighbor] = distances[item.value] + adj.weight
				heap.Push(&q, &Item{value: adj.neighbor, priority: distances[adj.neighbor]})
			}
		}
	}

	return distances
}

func main() {
	adjs, start, end, alternatives := ReadInput(os.Args[1])
	distances := Dijkstra([]int{start}, adjs)
	fmt.Printf("Solution 1: %d\n", distances[end])

	distances = Dijkstra(alternatives, adjs)
	fmt.Printf("Solution 2: %d\n", distances[end])

}
