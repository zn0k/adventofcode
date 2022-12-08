package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

type World [][]int
type Coordinate struct {
	X, Y int
}

func ExtractDigits(in string) []int {
	var result []int
	n, _ := strconv.Atoi(in)
	for n > 10 {
		result = append(result, n%10)
		n /= 10
	}
	result = append(result, n)
	for i := 0; i < len(result)/2; i++ {
		j := len(result) - i - 1
		result[i], result[j] = result[j], result[i]
	}
	return result
}

func ReadInput(path string) World {
	buf, err := ioutil.ReadFile(path)
	if err != nil {
		panic(fmt.Sprintf("unable to read from %s", path))
	}
	lines := strings.Split(string(buf), "\n")

	var world World
	for _, line := range lines {
		world = append(world, ExtractDigits(line))
	}
	return world
}

func FindHighPoints(world World) []Coordinate {
	tracker := make(map[Coordinate]bool)

	var result []Coordinate
	for key := range tracker {
		result = append(result, key)
	}
	return result
}

func main() {
	world := ReadInput(os.Args[1])
	fmt.Printf("%v\n", world)
}
