package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func readLines(path string) ([]int, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var fish []int

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		for _, field := range strings.Split(line, ",") {
			asInt, err := strconv.ParseInt(field, 10, 32)
			if err != nil {
				return nil, err
			}
			fish = append(fish, int(asInt))
		}
	}
	return fish, nil
}

func sumFish(fish *[]int) int {
	sum := 0
	for _, val := range *fish {
		sum += val
	}
	return sum
}

func main() {
	fishSeed, err := readLines(os.Args[1])
	if err != nil {
		panic(err)
	}

	// array to hold how many fish of a certain timer value exist
	fish := make([]int, 9)
	// sort the starting fish population into it
	for _, f := range fishSeed {
		fish[f]++
	}

	// step through the time range
	for day := 0; day < 256; day++ {
		// determine the number of fish about to spawn
		spawning := fish[0]
		// reduce the timer of all other fish by shifting them down an index
		for i := 1; i < 9; i++ {
			fish[i-1] = fish[i]
		}
		// add the fish that spawned back in with a timer of 6
		fish[6] += spawning
		// create the spawned fish with a timer of 8
		fish[8] = spawning

		// print the first solution if we're on iteration 80
		if day == 79 {
			fmt.Printf("Solution 1: %d\n", sumFish(&fish))
		}
	}

	fmt.Printf("Solution 2: %d\n", sumFish(&fish))
}
