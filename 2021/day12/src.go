package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"unicode"
	"unicode/utf8"
)

type Cave struct {
	name      string
	small     bool
	neighbors map[string]*Cave
}

func (c *Cave) HasNeighbor(v string) bool {
	_, exists := c.neighbors[v]
	return exists
}

func (c *Cave) AddNeighbor(n *Cave) {
	c.neighbors[n.name] = n
}

func MakeCave(v string) Cave {
	c := &Cave{}
	c.name = v
	first, _ := utf8.DecodeRuneInString(v)
	c.small = unicode.IsLower(first)
	c.neighbors = make(map[string]*Cave)
	return *c
}

type Map struct {
	m map[string]Cave
}

func (m *Map) Add(c Cave) {
	m.m[c.name] = c
}

func (m *Map) Contains(v string) bool {
	_, exists := m.m[v]
	return exists
}

func (m *Map) Get(v string) *Cave {
	c := m.m[v]
	return &c
}

func MakeWorld() Map {
	w := &Map{}
	w.m = make(map[string]Cave)
	return *w
}

type Tracker struct {
	t map[string]int
}

func (t *Tracker) Add(v string) {
	t.t[v] = 1
}

func (t *Tracker) IsValid(v string, allowRepeat bool) (bool, bool) {
	//fmt.Printf("Tracker.IsValid(%v) on %v with allow repeat %v: ", v, t.t, allowRepeat)
	first, _ := utf8.DecodeRuneInString(v)
	small := unicode.IsLower(first)
	_, seen := t.t[v]
	if seen && small {
		if allowRepeat {
			//fmt.Printf("allowing first repeat\n")
			return true, false
		} else {
			//fmt.Printf("small cave seen before\n")
			return false, allowRepeat
		}
	}
	//fmt.Printf("cave is big or hasn't been seen before\n")
	return true, allowRepeat
}

func (t *Tracker) Count() int {
	return len(t.t)
}

func (t *Tracker) Copy() Tracker {
	new := MakeTracker()
	for k := range t.t {
		new.Add(k)
	}
	return new
}

func MakeTracker() Tracker {
	t := &Tracker{}
	t.t = make(map[string]int)
	return *t
}

func readLines(p string) (Map, error) {
	w := MakeWorld()
	f, err := os.Open(p)
	if err != nil {
		return w, err
	}

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		fields := strings.Split(scanner.Text(), "-")
		left, right := fields[0], fields[1]
		if w.Contains(left) {
			c := w.Get(left)
			if !c.HasNeighbor(right) {
				if w.Contains(right) {
					n := w.Get(right)
					c.AddNeighbor(n)
					n.AddNeighbor(c)
				} else {
					n := MakeCave(right)
					w.Add(n)
					c.AddNeighbor(&n)
					n.AddNeighbor(c)
				}
			}
		} else {
			c := MakeCave(left)
			w.Add(c)
			if w.Contains(right) {
				n := w.Get(right)
				c.AddNeighbor(n)
				n.AddNeighbor(&c)
			} else {
				n := MakeCave(right)
				w.Add(n)
				c.AddNeighbor(&n)
				n.AddNeighbor(&c)
			}
		}
	}
	return w, scanner.Err()
}

func printWorld(w *Map) {
	for _, c := range w.m {
		fmt.Printf("Cave %s is small (%v) and has neighbors [", c.name, c.small)
		for _, n := range c.neighbors {
			fmt.Printf("%s, ", n.name)
		}
		fmt.Printf("]\n")
	}
}

func countPaths(c *Cave, t Tracker, allowRepeat bool, path string) int {
	path += "-" + c.name
	//fmt.Printf("countPaths called for cave %s, tracker %v, allowRepeat %v, path %s\n", c.name, t, allowRepeat, path)
	paths := 0
	if c.name == "end" {
		//fmt.Printf("Found a valid path!\n")
		return 1
	}
	if c.name == "start" && t.Count() > 0 {
		//fmt.Printf("Aborting, back at start\n")
		return 0
	}
	isValid, allowRepeat := t.IsValid(c.name, allowRepeat)
	if !isValid {
		//fmt.Printf("Have already been to cave too many time\n")
		return 0
	}
	t.Add(c.name)
	for _, n := range c.neighbors {
		//fmt.Printf("processing neighbor %s\n", n.name)
		nt := t.Copy()
		paths += countPaths(n, nt, allowRepeat, path)
	}
	return paths
}

func main() {
	world, err := readLines(os.Args[1])
	if err != nil {
		panic(err)
	}

	fmt.Printf("Solution 1: %d\n", countPaths(world.Get("start"), MakeTracker(), false, ""))
	fmt.Printf("Solution 2: %d\n", countPaths(world.Get("start"), MakeTracker(), true, ""))
}
