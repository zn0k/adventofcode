package main

import (
	"fmt"
	"intcode"
	"io/ioutil"
	"strings"

	"gonum.org/v1/gonum/stat/combin"
)

func runSequence(program string, sequence []int64) int64 {
	inA := make(chan int64, 2)
	outA := make(chan int64, 2)
	outB := make(chan int64, 2)
	outC := make(chan int64, 2)
	outD := make(chan int64, 2)
	outE := make(chan int64, 2)

	inA <- sequence[0]
	outA <- sequence[1]
	outB <- sequence[2]
	outC <- sequence[3]
	outD <- sequence[4]

	icA := intcode.New(inA, outA)
	icA.Load(strings.NewReader(program))
	inA <- 0
	go icA.Run()

	icB := intcode.New(outA, outB)
	icB.Load(strings.NewReader(program))
	go icB.Run()

	icC := intcode.New(outB, outC)
	icC.Load(strings.NewReader(program))
	go icC.Run()

	icD := intcode.New(outC, outD)
	icD.Load(strings.NewReader(program))
	go icD.Run()

	icE := intcode.New(outD, outE)
	icE.Load(strings.NewReader(program))
	go icE.Run()

	var last int64
	for result := range outE {
		last = result
		inA <- result
	}

	return last
}

func main() {
	buf, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic("Unable to read input.txt")
	}
	s := string(buf)

	sequence := []int64{0, 1, 2, 3, 4}
	sequence2 := []int64{5, 6, 7, 8, 9}
	var solution1 int64 = 0
	var solution2 int64 = 0
	for _, c := range combin.Permutations(5, 5) {
		var instance1 []int64
		var instance2 []int64
		for _, i := range c {
			instance1 = append(instance1, sequence[i])
			instance2 = append(instance2, sequence2[i])
		}
		result1 := runSequence(s, instance1)
		if result1 > solution1 {
			solution1 = result1
		}
		result2 := runSequence(s, instance2)
		if result2 > solution2 {
			solution2 = result2
		}
	}
	fmt.Printf("Solution 1: %d\n", solution1)
	fmt.Printf("Solution 2: %d\n", solution2)
}
