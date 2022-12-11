package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Monkey struct {
	Items   []int
	Inspect func(n int) int
	ThrowTo func(n int) int
}

type Game struct {
	Monkeys []*Monkey
	Worry   func(n int) int
}

func (game *Game) Play(rounds int) int {
	inspections := make([]int, len(game.Monkeys))

	for round := 0; round < rounds; round += 1 {
		for i, monkey := range game.Monkeys {
			for _, item := range monkey.Items {
				item = monkey.Inspect(item)
				item = game.Worry(item)
				to := monkey.ThrowTo(item)
				game.Monkeys[to].Items = append(game.Monkeys[to].Items, item)
				inspections[i] += 1
			}
			monkey.Items = []int{}
		}
	}

	sort.Ints(inspections)
	return inspections[len(inspections)-2] * inspections[len(inspections)-1]
}

func ReadInput(path string) ([]*Monkey, int) {
	buf, err := ioutil.ReadFile(path)
	if err != nil {
		panic(fmt.Sprintf("unable to read %s", path))
	}

	var monkeys []*Monkey
	lcm := 1

	for _, chunk := range strings.Split(string(buf), "\n\n") {
		var itemsStr, operator, target string
		var index, divisor, toTrue, toFalse int
		fmt.Sscanf(strings.ReplaceAll(chunk, ", ", ","), `Monkey %d:
  Starting items: %s
  Operation: new = old %s %s
  Test: divisible by %d
    If true: throw to monkey %d
    If false: throw to monkey %d`, &index, &itemsStr, &operator, &target, &divisor, &toTrue, &toFalse)

		lcm *= divisor

		var items []int
		for _, item := range strings.Split(itemsStr, ",") {
			i, _ := strconv.Atoi(item)
			items = append(items, i)
		}

		test := func(n int) int {
			if n%divisor == 0 {
				return toTrue
			}
			return toFalse
		}

		var op func(n int) int
		switch target {
		case "old":
			op = func(n int) int { return n * n }
		default:
			o, _ := strconv.Atoi(target)
			switch operator {
			case "+":
				op = func(n int) int { return n + o }
			case "*":
				op = func(n int) int { return n * o }
			}
		}

		monkeys = append(monkeys, &Monkey{Inspect: op, ThrowTo: test, Items: items})
	}
	return monkeys, lcm
}

func main() {
	monkeys, _ := ReadInput(os.Args[1])
	game1 := Game{Monkeys: monkeys, Worry: func(n int) int { return n / 3 }}
	fmt.Printf("Solution 1: %d\n", game1.Play(20))

	monkeys, lcm := ReadInput(os.Args[1])
	game2 := Game{Monkeys: monkeys, Worry: func(n int) int { return n % lcm }}
	fmt.Printf("Solution 2: %d\n", game2.Play(10000))
}
