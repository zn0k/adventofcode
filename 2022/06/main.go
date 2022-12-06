package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"

	"github.com/zn0k/gosets"
)

func Solve(chars []string, length int) int {
	result := 0
	for i := length - 1; i < len(chars); i += 1 {
		set := gosets.FromIterable(chars[i-length+1 : i+1])
		if set.Len() == length {
			result = i
			break
		}
	}
	return result + 1
}

func main() {
	buf, err := ioutil.ReadFile(os.Args[1])
	if err != nil {
		panic(fmt.Sprintf("unable to open %s for reading", os.Args[1]))
	}
	input := string(buf)
	chars := strings.Split(input, "")

	fmt.Printf("Solution 1: %d\n", Solve(chars, 4))
	fmt.Printf("Solution 2: %d\n", Solve(chars, 14))
}
