package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

const (
	_ = iota
	File
	Directory
)

type Kind int

type Node struct {
	Name     string
	Children []*Node
	Parent   *Node
	Size     int
	Kind     Kind
}

func NewNode(name string, kind Kind, parent *Node) *Node {
	n := &Node{Name: name, Kind: kind, Size: 0, Parent: parent}
	if kind == Directory {
		n.Children = make([]*Node, 0)
	}
	return n
}

func DFS(root *Node) []*Node {
	var nodes []*Node
	for _, child := range root.Children {
		if child.Kind == Directory {
			nodes = append(nodes, DFS(child)...)
		}
	}
	nodes = append(nodes, root)
	return nodes
}

func ReadInput(path string) *Node {
	f, err := os.Open(path)
	if err != nil {
		panic(fmt.Sprintf("unable to open %s for reading", path))
	}
	defer f.Close()

	root := NewNode("/", Directory, nil)
	current := root

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		fields := strings.Fields(scanner.Text())
		switch fields[0] {
		case "$": // it's a command
			switch fields[1] {
			case "cd": // cd'ing into a directory
				switch fields[2] {
				case "..": // move up, unless it's the root
					if current != root {
						current = current.Parent
					}
				default: // descend into a sub-directory by name
					for _, child := range current.Children {
						if child.Kind == Directory && child.Name == fields[2] {
							current = child
						}
					}
				}
			}
		case "dir": // it's a directory listing for a sub-directory
			child := NewNode(fields[1], Directory, current)
			current.Children = append(current.Children, child)
		default: // it's a directory listing for a file
			child := NewNode(fields[1], File, current)
			size, _ := strconv.Atoi(fields[0])
			child.Size = size
			current.Children = append(current.Children, child)
		}
	}

	return root
}

func CalculateSizes(root *Node) {
	// walk the DFS, summing up directory sizes as we go
	// this bubbles total sizes up to the root
	queue := DFS(root)
	for _, item := range queue {
		total := 0
		for _, child := range item.Children {
			total += child.Size
		}
		item.Size = total
	}
}

func main() {
	root := ReadInput(os.Args[1])
	CalculateSizes(root)

	part1 := 0
	var sizes []int
	for _, item := range DFS(root) {
		if item.Kind != Directory {
			continue
		}
		sizes = append(sizes, item.Size)
		if item.Size <= 100000 {
			part1 += item.Size
		}
	}
	fmt.Printf("Solution 1: %d\n", part1)

	needed := 30000000 - (70000000 - root.Size)
	sort.Ints(sizes)
	for _, s := range sizes {
		if s > needed {
			fmt.Printf("Solution 2: %d\n", s)
			break
		}
	}
}
