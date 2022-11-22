package main

import (
	"fmt"
	"intcode"
	"io/ioutil"
	"strings"
)

func main() {
	buf, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic("Unable to read input.txt")
	}
	s := string(buf)

	in := make(chan int64, 16)
	out := make(chan int64, 16)

	ic := intcode.New(in, out)
	ic.Load(strings.NewReader(s))
	in <- 1
	go ic.Run()

	solution1 := <-out

	fmt.Printf("Solution 1: %v\n", solution1)

	in = make(chan int64, 16)
	out = make(chan int64, 16)

	ic = intcode.New(in, out)
	ic.Load(strings.NewReader(s))
	in <- 2
	go ic.Run()

	solution2 := <-out

	fmt.Printf("Solution 2: %v\n", solution2)

}
