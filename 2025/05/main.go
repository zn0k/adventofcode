package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Range struct {
	start, end int64
}

func (r Range) contains(x int64) bool {
	return x >= r.start && x <= r.end
}

type Ranges struct {
	members []Range
}

func (rs Ranges) anyContains(x int64) bool {
	for _, r := range rs.members {
		if r.contains(x) {
			return true
		}
	}
	return false
}

func readFile(fname string) (Ranges, []int64) {
	file, _ := os.Open(fname)

	defer file.Close()

	ranges := make([]Range, 0)
	ingredients := make([]int64, 0)

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		// skip empty lines
		if len(line) == 0 {
			continue
		}
		// if there's a -, it's a range
		if strings.Contains(line, "-") {
			// split into fields
			fields := strings.Split(line, "-")
			// blindly convert to a number
			start, _ := strconv.Atoi(fields[0])
			end, _ := strconv.Atoi(fields[1])
			ranges = append(ranges, Range{int64(start), int64(end)})
		} else {
			// ingredient, convert to a number
			ingredient, _ := strconv.Atoi(line)
			ingredients = append(ingredients, int64(ingredient))
		}
	}

	return Ranges{ranges}, ingredients
}

// for each ingredient, walk ranges to see if any of them
// contain it
func findSolution(ranges Ranges, ingredients []int64) int64 {
	var result int64 = 0
	for _, i := range ingredients {
		if ranges.anyContains(i) {
			result += 1
		}
	}
	return result
}

func main() {
	ranges, ingredients := readFile("input.txt")
	solution1 := findSolution(ranges, ingredients)

	// sort the ranges by start number
	sorted := ranges.members
	sort.Slice(sorted, func(i, j int) bool { return sorted[i].start < sorted[j].start })

	merged := make([]Range, 0)
	merged = append(merged, sorted[0])

	// walk the ranges and merge them if there's overlap
	for i := 1; i < len(sorted); i++ {
		// no overlap, new range starts after last one ends
		if sorted[i].start > merged[len(merged)-1].end {
			// add it to the list
			merged = append(merged, sorted[i])
		} else {
			// overlap, reset the end number of the last range to the maximum
			// of the two
			merged[len(merged)-1].end = max(sorted[i].end, merged[len(merged)-1].end)
		}
	}

	// walk the ranges and sum up what they cover
	var solution2 int64 = 0
	for _, r := range merged {
		solution2 += r.end - r.start + 1
	}

	fmt.Printf("Solution 1: %d\nSolution 2: %d\n", solution1, solution2)

}
