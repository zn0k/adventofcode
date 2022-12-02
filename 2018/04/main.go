package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
	"time"
)

const (
	_ = iota
	SHIFTSTART
	SLEEPS
	WAKES
)

type Event struct {
	GuardID   int
	Timestamp time.Time
	Action    int
}

type Events []Event

func (es Events) Len() int {
	return len(es)
}

func (es Events) Swap(i, j int) {
	es[i], es[j] = es[j], es[i]
}

func (es Events) Less(i, j int) bool {
	return es[i].Timestamp.Before(es[j].Timestamp)
}

func ParseDate(s string) time.Time {
	ss := strings.Split(s, " ")
	cs := strings.Split(ss[0], "-")
	cs = append(cs, strings.Split(ss[1], ":")...)

	var ds []int
	for _, c := range cs {
		i, _ := strconv.Atoi(c)
		ds = append(ds, i)
	}

	return time.Date(ds[0], time.Month(ds[1]), ds[2], ds[3], ds[4], 0, 0, time.UTC)
}

func GetInput(path string) Events {
	f, err := os.Open(path)
	if err != nil {
		panic(fmt.Sprintf("unable to open %s for reading", path))
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)
	var events Events
	for scanner.Scan() {
		words := strings.Fields(scanner.Text())
		d := strings.TrimPrefix(words[0], "[")
		t := strings.TrimSuffix(words[1], "]")
		var action int
		guardId := 0

		switch words[2] {
		case "Guard":
			action = SHIFTSTART
			id := strings.TrimPrefix(words[3], "#")
			guardId, _ = strconv.Atoi(id)
		case "wakes":
			action = WAKES
		case "falls":
			action = SLEEPS
		default:
			panic(fmt.Sprintf("unknown guard action '%s'", strings.Join(words[2:], "")))
		}

		events = append(events, Event{
			GuardID:   guardId,
			Timestamp: ParseDate(d + " " + t),
			Action:    action,
		})
	}

	return events
}

func main() {
	events := GetInput(os.Args[1])
	sort.Sort(events)

	// data structure to map a guard's ID against a map of how many times
	// they were sleeping at a given minute
	lookup := make(map[int]map[int]int)

	// pre-populate all minutes for all guards to make lookups easier and faster
	for _, e := range events {
		if e.Action == SHIFTSTART {
			_, ok := lookup[e.GuardID]
			if !ok {
				minutes := make(map[int]int)
				for m := 0; m < 60; m += 1 {
					minutes[m] = 0
				}
				lookup[e.GuardID] = minutes
			}
		}
	}

	var guardId int
	var sleepStart int
	for _, e := range events {
		switch e.Action {
		case SHIFTSTART:
			guardId = e.GuardID
		case SLEEPS:
			sleepStart = e.Timestamp.Minute()
		case WAKES:
			for i := sleepStart; i < e.Timestamp.Minute(); i += 1 {
				lookup[guardId][i] += 1
			}
		}
	}

	// determine winner for both solutions
	p1winner := -1
	p2winner := -1
	p1max := -1
	p2max := -1
	p2min := -1
	for id, minutes := range lookup {
		sleep := 0
		for minute, slept := range minutes {
			sleep += slept
			if slept > p2max {
				p2max = slept
				p2min = minute
				p2winner = id
			}
		}
		if sleep > p1max {
			p1max = sleep
			p1winner = id
		}
	}

	// figure out which minute winner for solution 1 slept the most
	maxMinute := -1
	max := -1
	for minute, slept := range lookup[p1winner] {
		if slept > max {
			max = slept
			maxMinute = minute
		}
	}

	fmt.Printf("Solution 1: %d\nSolution 2: %d\n", p1winner*maxMinute, p2winner*p2min)
}
