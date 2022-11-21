package main

import (
	"fmt"
	"intcode"
	"io/ioutil"
	"strings"
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
	icA.Run()

	icB := intcode.New(outA, outB)
	icB.Load(strings.NewReader(program))
	icB.Run()

	icC := intcode.New(outB, outC)
	icC.Load(strings.NewReader(program))
	icC.Run()

	icD := intcode.New(outC, outD)
	icD.Load(strings.NewReader(program))
	icD.Run()

	icE := intcode.New(outD, outE)
	icE.Load(strings.NewReader(program))
	icE.Run()

	result := <-outE

	return result
}

func main() {
	buf, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic("Unable to read input.txt")
	}
	s := string(buf)

	// loop through all permnutations, find highest result
	result := runSequence(s, []int64{4, 3, 2, 1, 0})
	fmt.Println(result)
}
