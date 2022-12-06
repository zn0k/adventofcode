package main

import (
	"container/list"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

type Node struct {
	Children       int
	Metadata       int
	ChildrenParsed int
}

func ReadInput(path string) []int {
	buf, err := ioutil.ReadFile(path)
	if err != nil {
		panic(fmt.Sprintf("unable to open %s for reading", path))
	}

	var result []int
	for _, field := range strings.Fields(string(buf)) {
		num, _ := strconv.Atoi(field)
		result = append(result, num)
	}

	return result
}

func SumTree(tree []int) int {
	// need at least one valid entry in the tree
	if len(tree) <= 2 {
		return 0
	}

	sum := 0
	end := len(tree)
	// create a stack and put the root element on it
	stack := list.New()
	stack.PushBack(Node{Children: tree[0], Metadata: tree[1], ChildrenParsed: 0})
	count := 0

	// start parsing the tree at index 2, where either the first child or the first metadata sits
	for i := 2; stack.Back() != nil; {
		var node Node
		fmt.Printf("beginning of loop, at index %d\n", i)
		for {
			// get the current element
			e := stack.Back()
			node, _ = e.Value.(Node)
			fmt.Printf("retrieved node %v\n", node)
			// check if the current node has more children to be parsed
			if node.Children-node.ChildrenParsed == 0 {
				// all its children have been parsed, so get the metadata values and add to the sum
				metaEnd := i + node.Metadata
				for ; i < metaEnd; i += 1 {
					sum += tree[i]
				}
				// node is done, remove it from the stack
				stack.Remove(e)
				fmt.Printf("all children done, read node metadata, sum is now %d, index %d\n", sum, i)
				// mark a child as read
				e = stack.Back()
				node, _ = e.Value.(Node)
				node.ChildrenParsed += 1
			} else {
				fmt.Printf("node still has %d children to parse\n", node.Children-node.ChildrenParsed)
				break
			}
		}
		// check if there is still data to parse
		if i < end {
			// next is a new node
			children := tree[i]
			metadata := tree[i+1]
			// move the index forward
			i += 2
			// mark that a child of the current element has been parsed
			node.ChildrenParsed += 1
			// push the new node to the stack
			child := Node{Children: children, Metadata: metadata, ChildrenParsed: 0}
			stack.PushBack(child)
			fmt.Printf("added new child node %v, index %d\n", child, i)
		}
		count += 1
		if count > 10 {
			break
		}
	}

	return sum
}

func main() {
	tree := ReadInput(os.Args[1])
	fmt.Printf("%v\n", tree)

	sum := SumTree(tree)
	fmt.Printf("Solution 1: %d\n", sum)
}
