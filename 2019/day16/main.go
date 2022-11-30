package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"strconv"
	"strings"
)

func StringToSlice(s string) []int {
	result := make([]int, len(s))
	for i, r := range s {
		num, err := strconv.ParseInt(string(r), 10, 32)
		if err != nil {
			panic("unable to parse digit as integer")
		}
		result[i] = int(num)
	}
	return result
}

func Process(signal []int, iterations int) []int {
	l := len(signal)
	temp := make([]int, l)

	for iteration := 0; iteration < iterations; iteration++ {
		for digit := 0; digit < l; digit++ {
			sum := 0
			index := digit
			for index < l {
				for i := 0; i <= digit; i++ {
					if index+i >= l {
						break
					}
					sum += signal[index+i]
				}
				index += (digit + 1) * 4
			}
			index = digit + (2 * (digit + 1))
			for index < l {
				for i := 0; i <= digit; i++ {
					if index+i >= l {
						break
					}
					sum -= signal[index+i]
				}
				index += (digit + 1) * 4
			}
			temp[digit] = int(math.Abs(float64(sum))) % 10
		}
		signal = temp
	}
	if len(signal) > 8 {
		return signal[0:8]
	} else {
		return signal
	}
}

func Stringify(digits []int) string {
	result := ""
	for _, d := range digits {
		result += strconv.FormatInt(int64(d), 10)
	}
	return result
}

func main() {
	buf, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic("unable to open input.txt")
	}
	input_string := string(buf)
	signal := StringToSlice(input_string)
	result := Process(signal, 100)
	fmt.Printf("Solution 1: %s\n", Stringify(result))

	input_string = strings.Repeat(input_string, 10000)
	signal = StringToSlice(input_string)
	result = Process2(signal, 100)
	fmt.Printf("Solution 2: %s\n", Stringify(result))
}

func Process2(signal []int, iterations int) []int {
	l := len(signal)
	temp := make([]int, l)

	// calculate the offset based on the first 7 digits
	offset := 0
	for i := 0; i < 7; i++ {
		offset += (signal[i] * int(math.Pow10(7-i-1)))
	}

	// sum up digits from the end. this won't let us get the whole signal
	// it will, however, let us get the last half of them for each iteration
	// that's because the filter pattern at the half way point is 0...01...1
	// the last filter is 0...01, so the last digit is the same as from the input
	// the second to last is the new last digit + the second to last signal digit mod 10
	// the third to last is the previous sum plus the third to last from the signal mod 10, and so on

	// the offset is in the second half, so this works
	for i := 0; i < iterations; i++ {
		sum := signal[l-1]
		temp[l-1] = sum
		for digit := l - 2; digit >= l/2; digit-- {
			sum += signal[digit]
			d := sum % 10
			temp[digit] = d
		}
		signal = temp
	}

	return signal[offset : offset+8]
}
