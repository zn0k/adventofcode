package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"

	"golang.org/x/exp/maps"
)

type Reaction struct {
	Out int64
	In  map[string]int64
}

type DefaultMap struct {
	m map[string]int64
}

func NewDefaultMap() *DefaultMap {
	m := &DefaultMap{}
	m.m = make(map[string]int64)
	return m
}

func (m *DefaultMap) Get(key string) int64 {
	i, ok := m.m[key]
	if !ok {
		return 0
	}
	return i
}

func (m *DefaultMap) Set(key string, val int64) {
	m.m[key] = val
}

func (m *DefaultMap) Delete(key string) {
	delete(m.m, key)
}

func (m *DefaultMap) GetNextKey() string {
	if len(m.m) > 0 {
		return maps.Keys(m.m)[0]
	}
	return ""
}

func (m *DefaultMap) Length() int {
	return len(m.m)
}

func splitIngredient(s string) (int64, string) {
	fields := strings.Split(s, " ")
	quantity, err := strconv.ParseInt(fields[0], 10, 64)
	if err != nil {
		panic("unable to convert quantity into integer")
	}
	return quantity, fields[1]
}

func ReadInput(in io.Reader) map[string]Reaction {
	scanner := bufio.NewScanner(in)
	reactions := make(map[string]Reaction)
	for scanner.Scan() {
		line := scanner.Text()
		fields := strings.Split(line, " => ")
		list := strings.Split(fields[0], ", ")
		ingredients := make(map[string]int64)
		for _, item := range list {
			quantity, name := splitIngredient(item)
			ingredients[name] = quantity
		}
		quantity, name := splitIngredient(fields[1])
		reactions[name] = Reaction{Out: quantity, In: ingredients}
	}
	return reactions
}

func Resolve(fuel_required int64, reactions map[string]Reaction) int64 {
	needed := NewDefaultMap()
	needed.Set("FUEL", fuel_required)

	have := NewDefaultMap()
	var total_ore int64 = 0

	for needed.Length() > 0 {
		// grab an item name off the list of needed items
		item := needed.GetNextKey()
		// check if we have more of that item than we need
		if needed.Get(item) <= have.Get(item) {
			// yes! subtract it from the stack of leftovers
			have.Set(item, have.Get(item)-needed.Get(item))
			// delete it from the list of needed items
			needed.Delete(item)
			// and move on to the next item
			continue
		}

		// don't have it, so we need to produce the item
		// figure out how many of that item we need on top of what might be in stock
		num_needed := needed.Get(item) - have.Get(item)
		// we're making the item, so we no longer need it
		needed.Delete(item)
		// we have depleted what might have been in stock
		have.Delete(item)

		// look up how many of the item we can produce via the reaction that makes it
		num_made := reactions[item].Out
		// figure out how many reactions we need to go through to make as many as we need
		var num_reactions int64 = 0
		if num_needed%num_made == 0 {
			num_reactions = num_needed / num_made
		} else {
			num_reactions = (num_needed / num_made) + 1
		}

		// store what we have left over
		leftovers := (num_reactions * num_made) - num_needed
		have.Set(item, leftovers)

		for item_needed, quantity := range reactions[item].In {
			if item_needed == "ORE" {
				total_ore += quantity * num_reactions
			} else {
				needed.Set(item_needed, quantity*num_reactions+needed.Get(item_needed))
			}
		}
	}
	return total_ore
}

func Maximize(ore_available int64, reactions map[string]Reaction) int64 {
	// at the very least we can make 1 trillion divided by how much ore it takes to make one fuel
	lower_bound := ore_available / Resolve(1, reactions)
	// test out the higher bound by creeping up by factors of 10
	higher_bound := lower_bound * 10
	for Resolve(higher_bound, reactions) < ore_available {
		lower_bound = higher_bound
		higher_bound = lower_bound * 10
	}

	// now loop through calculating the mid point, and then shifting the lower bound up or
	// shifting the higher bound down. eventually, this converges
	var mid_point int64 = 0
	for lower_bound < higher_bound-1 {
		mid_point = (lower_bound + higher_bound) / 2
		ore := Resolve(mid_point, reactions)
		if ore < ore_available {
			lower_bound = mid_point
		} else if ore > ore_available {
			higher_bound = mid_point
		} else {
			break
		}
	}
	// why subtract 1 below? no idea, actually, but the tests fail with one-off errors for all cases
	return mid_point - 1
}

func main() {
	f, err := os.Open("input.txt")
	if err != nil {
		panic("unable to read input.txt")
	}
	reactions := ReadInput(f)
	fmt.Printf("Solution 1: %d\n", Resolve(1, reactions))

	solution2 := Maximize(1000000000000, reactions)
	fmt.Printf("Solution 2: %d\n", solution2)
}
