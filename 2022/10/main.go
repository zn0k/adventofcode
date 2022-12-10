package main

import (
	"fmt"
	"image"
	"image/png"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

func main() {
	buf, err := ioutil.ReadFile(os.Args[1])
	if err != nil {
		panic(fmt.Sprintf("unable to read %s", os.Args[1]))
	}

	registerValues := []int{1}
	idx := 0
	for _, line := range strings.Split(string(buf), "\n") {
		fields := strings.Fields(line)
		switch fields[0] {
		case "noop":
			registerValues = append(registerValues, registerValues[idx])
			idx += 1
		case "addx":
			val, _ := strconv.Atoi(fields[1])
			registerValues = append(registerValues, registerValues[idx], registerValues[idx]+val)
			idx += 2
		}
	}

	sum := 0
	for i := 20; i < len(registerValues); i += 40 {
		sum += registerValues[i-1] * i
	}

	var screen string
	for i := 0; i < len(registerValues); i += 1 {
		pos := i % 40
		pixel := "."
		if pos >= registerValues[i]-1 && pos <= registerValues[i]+1 {
			pixel = "#"
		}
		screen += pixel
		if pos == 39 {
			screen += "\n"
		}
	}

	width, height := image.Point{0, 0}, image.Point{40 * 4, (len(registerValues) / 40) * 4}
	img := image.NewRGBA(image.Rectangle{width, height})
	for i := 0; i < len(registerValues); i += 1 {
		pos := i % 40
		color := image.White
		if pos >= registerValues[i]-1 && pos <= registerValues[i]+1 {
			color = image.Black
		}
		for x := 0; x < 4; x += 1 {
			for y := 0; y < 4; y += 1 {
				img.Set(pos*4+x, (i/40)*4+y, color)
			}
		}
	}
	f, _ := os.Create("day10.png")
	png.Encode(f, img)

	fmt.Printf("Solution 1: %d\nSolution 2:\n%s\n", sum, screen)
}
