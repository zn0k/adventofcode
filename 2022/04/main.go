package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"

	"github.com/zn0k/gosets"
)

type Pair struct {
	A, B []int
}

func ReadInput(path string) []Pair {
	f, err := os.Open(path)
	if err != nil {
		panic(fmt.Sprintf("unable to open %s for reading", path))
	}
	defer f.Close()

	var pairs []Pair

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		fields := strings.Split(scanner.Text(), ",")
		words := strings.Split(fields[0], "-")
		words = append(words, strings.Split(fields[1], "-")...)
		var nums []int
		for _, num := range words {
			i, _ := strconv.Atoi(num)
			nums = append(nums, i)
		}
		var rangeA, rangeB []int
		for i := nums[0]; i <= nums[1]; i++ {
			rangeA = append(rangeA, i)
		}
		for i := nums[2]; i <= nums[3]; i++ {
			rangeB = append(rangeB, i)
		}
		pairs = append(pairs, Pair{rangeA, rangeB})
	}

	return pairs
}

func Count(pairs *[]Pair) (int, int) {
	contained := 0
	overlap := 0

	for _, pair := range *pairs {
		a := gosets.New[int]()
		b := gosets.New[int]()
		a.AddMany(pair.A)
		b.AddMany(pair.B)
		if a.IsSubset(b) || b.IsSubset(a) {
			contained += 1
		}
		if !a.IsDisjoint(b) {
			overlap += 1
		}
	}

	return contained, overlap
}

func main() {
	pairs := ReadInput(os.Args[1])
	contained, overlap := Count(&pairs)

	fmt.Printf("Solution 1: %d\nSolution 2: %d\n", contained, overlap)
}
