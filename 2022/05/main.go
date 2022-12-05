package main

import (
	"container/list"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

type Move struct {
	From     int
	To       int
	Quantity int
}

func ParseStacks(input string) []*list.List {
	// split by lines, and trim off the last one that counts the columns
	lines := strings.Split(input, "\n")
	lines = lines[0 : len(lines)-1]
	// calculate number of columns
	columns := (len(lines[0]) / 4) + 1

	// create the stacks as DLLs
	stacks := make([]*list.List, columns)
	for i := 0; i < columns; i += 1 {
		stacks[i] = list.New()
	}

	// parse the lines into the stack bottom up to make the logic easier
	for i := len(lines) - 1; i >= 0; i -= 1 {
		column := 0
		// first box is at index 1, then every 4 chars is a box
		for j := 1; j < len(lines[i]); j += 4 {
			char := string(lines[i][j])
			// if there's a non-space character at that index, add box to the stack
			if char != " " {
				stacks[column].PushBack(char)
			}
			column += 1
		}
	}
	return stacks
}

func ParseMoves(input string) []Move {
	var moves []Move
	for _, line := range strings.Split(input, "\n") {
		var nums []int
		fields := strings.Fields(line)
		for _, index := range []int{1, 3, 5} {
			i, _ := strconv.Atoi(fields[index])
			nums = append(nums, i)
		}
		moves = append(moves, Move{From: nums[1] - 1, To: nums[2] - 1, Quantity: nums[0]})
	}

	return moves
}

func ReadInput(path string) ([]*list.List, []Move) {
	buf, err := ioutil.ReadFile(path)
	if err != nil {
		panic(fmt.Sprintf("unable to read file %s", path))
	}

	parts := strings.Split(string(buf), "\n\n")

	return ParseStacks(parts[0]), ParseMoves(parts[1])
}

func MakeMove(stacks []*list.List, move Move) {
	for i := 0; i < move.Quantity; i += 1 {
		box := stacks[move.From].Back()
		stacks[move.To].PushBack(box.Value)
		stacks[move.From].Remove(box)
	}
}

func MakeMove9001(stacks []*list.List, move Move) {
	tmp := list.New()
	for i := 0; i < move.Quantity; i += 1 {
		box := stacks[move.From].Back()
		tmp.PushBack(box.Value)
		stacks[move.From].Remove(box)
	}
	for i := 0; i < move.Quantity; i += 1 {
		box := tmp.Back()
		stacks[move.To].PushBack(box.Value)
		tmp.Remove(box)
	}
}

func GetMessage(stacks []*list.List) string {
	msg := ""
	for _, stack := range stacks {
		msg += stack.Back().Value.(string)
	}
	return msg
}

func main() {
	stacks, moves := ReadInput(os.Args[1])
	for _, move := range moves {
		MakeMove(stacks, move)
	}
	fmt.Printf("Solution 1: %s\n", GetMessage(stacks))

	stacks, moves = ReadInput(os.Args[1])
	for _, move := range moves {
		MakeMove9001(stacks, move)
	}
	fmt.Printf("Solution 2: %s\n", GetMessage(stacks))
}
