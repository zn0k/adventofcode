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
	ic.Run()
	var last int64
	for {
		val, ok := <-out
		if !ok {
			break
		} else {
			last = val
		}
	}
	fmt.Printf("Solution 1: %d\n", last)

	in = make(chan int64, 1)
	out = make(chan int64, 1)
	ic = intcode.New(in, out)
	ic.Load(strings.NewReader(s))
	in <- 5
	ic.Run()
	result := <-out
	fmt.Printf("Solution 2: %d\n", result)
}
