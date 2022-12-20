package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

func ReadInput(path string) []int64 {
	buf, _ := ioutil.ReadFile(path)
	lines := strings.Split(string(buf), "\n")
	nums := make([]int64, len(lines))
	for i := 0; i < len(lines); i += 1 {
		num, _ := strconv.ParseInt(lines[i], 10, 64)
		nums[i] = num
	}
	return nums
}

func Index(limit int, predicate func(i int) bool) int {
	for i := 0; i < limit; i += 1 {
		if predicate(i) {
			return i
		}
	}
	return -1
}

func Insert(a []int, idx, val int) []int {
	if len(a) == idx {
		return append(a, val)
	}
	a = append(a[:idx+1], a[idx:]...)
	a[idx] = val
	return a
}

// go does modulo different from python this took a while
// https://stackoverflow.com/questions/43018206/modulo-of-negative-integers-in-go
func nnmod(a, b int64) int {
	return int((a%b + b) % b)
}

func Mix(nums []int64, n int) []int64 {
	idx := make([]int, len(nums))
	for i := 0; i < len(nums); i += 1 {
		idx[i] = i
	}
	for times := 0; times < n; times += 1 {
		for i, v := range nums {
			if v == 0 {
				continue
			}
			j := Index(len(nums), func(a int) bool { return idx[a] == i })
			x := idx[j]
			idx := append(idx[:j], idx[j+1:]...)
			k := nnmod(int64(j)+v, int64(len(nums)-1))
			idx = Insert(idx, k, x)
		}
	}
	mixed := make([]int64, len(nums))
	for i, v := range idx {
		mixed[i] = nums[v]
	}
	return mixed
}

func Coordinates(nums []int64) int64 {
	i := Index(len(nums), func(a int) bool { return nums[a] == 0 })
	sum := int64(0)
	for _, n := range []int{1000, 2000, 3000} {
		sum += nums[(i+n)%len(nums)]
	}
	return sum
}

func main() {
	input := ReadInput(os.Args[1])
	fmt.Printf("Solution 1: %d\n", Coordinates(Mix(input, 1)))

	decrypted := make([]int64, len(input))
	for i := 0; i < len(input); i += 1 {
		decrypted[i] = input[i] * 811589153
	}
	fmt.Printf("Solution 2: %d\n", Coordinates(Mix(decrypted, 10)))
}
