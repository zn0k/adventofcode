package main

import (
	"container/list"
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"strings"
	"unicode"
)

func ReadInput(path string) string {
	buf, err := ioutil.ReadFile(path)
	if err != nil {
		panic(fmt.Sprintf("unable to read '%s'", path))
	}
	return strings.TrimSpace(string(buf))
}

func MakeList(input string) *list.List {
	polymer := list.New()
	for _, unit := range input {
		polymer.PushBack(string(unit))
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

func GetElements(p *list.List) []rune {
	lookup := make(map[rune]bool)
	for e := p.Front(); e.Next() != nil; e = e.Next() {
		value := e.Value.(string)
		letter := unicode.ToLower(rune(value[0]))
		lookup[letter] = true
	}

	var result []rune
	for letter, _ := range lookup {
		result = append(result, letter)
	}

	return result
}

func RemoveUnit(p *list.List, lowerCase rune) {
	upperCase := unicode.ToUpper(lowerCase)
	for e := p.Front(); e.Next() != nil; {
		if e.Value == string(lowerCase) || e.Value == string(upperCase) {
			if e == p.Front() {
				p.Remove(e)
				e = p.Front()
			} else {
				prev := e.Prev()
				p.Remove(e)
				e = prev
			}
		} else {
			e = e.Next()
		}
	}
}

func main() {
	input := ReadInput(os.Args[1])
	polymer := MakeList(input)
	React(polymer)
	fmt.Printf("Solution 1: %d\n", polymer.Len())

	elements := GetElements(polymer)
	minimum := math.MaxInt32
	for _, elem := range elements {
		polymer = MakeList(input)
		RemoveUnit(polymer, elem)
		React(polymer)
		if polymer.Len() < minimum {
			minimum = polymer.Len()
		}
	}
	fmt.Printf("Solution 2: %d\n", minimum)
}
