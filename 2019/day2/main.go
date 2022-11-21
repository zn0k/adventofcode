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

	in := make(chan int64, 2)
	out := make(chan int64, 2)
	ic := intcode.New(in, out)
	ic.Load(strings.NewReader(s))
	ic.Write(1, 12)
	ic.Write(2, 2)
	ic.Run()
	fmt.Printf("Solution 1: %d\n", ic.Read(0))

BREAK:
	for noun := int64(0); noun <= 99; noun++ {
		for verb := int64(0); verb <= 99; verb++ {
			in = make(chan int64, 2)
			out = make(chan int64, 2)
			ic = intcode.New(in, out)
			ic.Load(strings.NewReader(s))
			ic.Write(1, noun)
			ic.Write(2, verb)
			ic.Run()
			if ic.Read(0) == 19690720 {
				fmt.Printf("Solution 2: %d\n", 100*noun+verb)
				continue BREAK
			}
		}
	}
}
