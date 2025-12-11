package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

// read in the file, returning a map of nodes
// against the list of nodes they connect to
func readFile(fname string) map[string][]string {
	file, _ := os.Open(fname)

	defer file.Close()

	adj := make(map[string][]string)

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		fields := strings.Split(scanner.Text(), ": ")
		adj[fields[0]] = strings.Split(fields[1], " ")
	}

	return adj
}

// kahn's algorithm to topologically sort an adjancency map
func topological_order(adj map[string][]string) []string {
	// compute in-degrees, and also create a set of node names
	indeg := make(map[string]int64)
	// create the set of node names
	nodes := make(map[string]bool)
	for u, neighbors := range adj {
		// add u to the set
		nodes[u] = true
		// walk u's neighbors
		for _, v := range neighbors {
			// add v to the set
			nodes[v] = true
			// add an in-degree for v
			indeg[v] += 1
		}
	}
	// use a slice as a queue - this isn't a huge graph, so performance
	// for this shouldn't matter much
	q := make([]string, 0)
	// and allocate the data structure for the ordered list of nodes
	order := make([]string, 0)

	// and add the nodes that don't have in-degrees to the queue
	// as they come first in the sort order and can be used as starters
	for u, _ := range nodes {
		if _, ok := indeg[u]; !ok {
			q = append(q, u)
		}
	}

	// keep processing while there's queue elements
	for len(q) != 0 {
		// popleft
		u := q[0]
		q = q[1:]
		// this node is next in the order
		order = append(order, u)
		// walk its neighbors
		for _, v := range adj[u] {
			// reduce the neighbors in-degree by one
			indeg[v] -= 1
			// if it's down to zero, throw it into the queue for processing
			if indeg[v] == 0 {
				q = append(q, v)
			}
		}
	}

	return order
}

func count_paths(adj map[string][]string, source, target string) int64 {
	topology := topological_order(adj)

	// create a data structure to count the number of paths
	paths := make(map[string]int64)
	for _, u := range topology {
		paths[u] = 0
	}
	// if the source isn't in the adjancency map, bail
	if _, ok := paths[source]; !ok {
		return 0
	}
	// seed the counter for the source
	paths[source] = 1

	// and walk
	for _, u := range topology {
		for _, v := range adj[u] {
			// propagate the path counts to neighbors
			paths[v] += paths[u]
		}
	}

	return paths[target]
}

func main() {
	adj := readFile("input.txt")
	// count the paths from you to out
	solution1 := count_paths(adj, "you", "out")

	// count the paths from svr to out that go through fft and dac
	// do this in segments, and account for the two possible
	// waypoint orderings
	solution2_a := count_paths(adj, "svr", "fft")
	solution2_a *= count_paths(adj, "fft", "dac")
	solution2_a *= count_paths(adj, "dac", "out")

	solution2_b := count_paths(adj, "svr", "dac")
	solution2_b *= count_paths(adj, "dac", "fft")
	solution2_b *= count_paths(adj, "fft", "out")

	solution2 := solution2_a + solution2_b

	fmt.Printf("Solution 1: %d\nSolution 2: %d\n", solution1, solution2)
}
