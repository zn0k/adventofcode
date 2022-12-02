package main

import (
	"bufio"
	"container/list"
	"fmt"
	"os"
	"unicode"
)

func ReadInput(path string) *list.List {
	f, err := os.Open(path)
	if err != nil {
		panic(fmt.Sprintf("unable to open '%s' for reading", path))
	}
	defer f.Close()

	polymer := list.New()

	scanner := bufio.NewScanner(f)
	scanner.Split(bufio.ScanRunes)
	for scanner.Scan() {
		unit := scanner.Text()
		polymer.PushBack(unit)
	}

	return polymer
}

func Toggle(r string) string {
	letter := rune(r[0])
	if unicode.IsUpper(letter) {
		return string(unicode.ToLower(letter))
	}
	return string(unicode.ToUpper(letter))
}

func React(p *list.List) {
	for e := p.Front(); e != nil; {
		if e.Next() != nil {
			// compare the value of the current element and the next one
			current := e.Value
			next := Toggle(e.Next().Value.(string))
			if current == next {
				// have a match. check what kind of movement should occur
				if e == p.Front() {
					// we're at the head of the list, so remove this pair and reset to the front
					p.Remove(e.Next())
					p.Remove(e)
					e = p.Front()
				} else if e.Prev() == p.Front() {
					// we're one element in, delete this pair and move back to the head of the list
					p.Remove(e.Next())
					p.Remove(e)
					e = p.Front()
				} else {
					// we're at least two elements in
					prev := e.Prev().Prev()
					p.Remove(e.Next())
					p.Remove(e)
					e = prev
				}
			} else {
				// not a match, move forward to the next element
				e = e.Next()
			}
		} else {
			break
		}
	}
}

func PrintPolymer(p *list.List) string {
	result := ""
	for e := p.Front(); e != nil; e = e.Next() {
		result += e.Value.(string)
	}
	return result
}

func main() {
	polymer := ReadInput(os.Args[1])
	React(polymer)
	fmt.Printf("Solution 1: %d\n", polymer.Len())
}
