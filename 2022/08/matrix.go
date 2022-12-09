// re-implementation of part 1 using matrices from gonum just to learn it a little bit

package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"

	"gonum.org/v1/gonum/mat"
)

var minor *mat.Dense

func ReadInputMatrix(path string) *mat.Dense {
	buf, err := ioutil.ReadFile(path)
	if err != nil {
		panic(fmt.Sprintf("unable to read from %s", path))
	}
	lines := strings.Split(string(buf), "\n")

	var data []float64
	for _, line := range lines {
		for _, c := range line {
			i, _ := strconv.Atoi(string(c))
			data = append(data, float64(i))
		}
	}
	return mat.NewDense(len(lines), len(data)/len(lines), data)
}

func CreateMinor(height, width int) {
	// create minor diagonal of right dimensions
	var swaps []int
	for i := height - 1; i >= 0; i -= 1 {
		swaps = append(swaps, i)
	}
	minor = mat.NewDense(height, width, nil)
	minor.Permutation(height, swaps)
}

// rotate a given matrix left by 90 degrees
func Rotate(a *mat.Dense) {
	a.Mul(a.T(), minor)
}

// create a matrix where row elements increase monotonically from the left
func Monotonic(a *mat.Dense) *mat.Dense {
	height, width := a.Dims()
	result := mat.NewDense(height, width, nil)
	result.CloneFrom(a)
	// run through the slices that back each row, and record the max seen so far
	for i := 0; i < height; i += 1 {
		row := result.RawRowView(i)
		max := row[0]
		for j := 1; j < len(row)-1; j += 1 {
			if row[j] > max {
				tmp := row[j]
				row[j] = max
				max = tmp
			} else {
				row[j] = max
			}
		}
		row[0] = 1.0
		row[len(row)-1] = 1.0
	}

	return result
}

// take in a value in a matrix and return 1.0 if it's more than 0, and 0.0 otherwise
func Normalize(i, j int, v float64) float64 {
	if v > 0.0 {
		return 1.0
	}
	return 0.0
}

func CountHighPoints(world *mat.Dense) int {
	height, width := world.Dims()
	visibleTotal := mat.NewDense(height, width, nil)

	// look at world from all 4 directions by rotating it 90 degrees 4 times
	for range []int{1, 2, 3, 4} {
		// create a matrix where the monotic increase is subtracted from the world,
		// yielding a non-zero value for each tree that is visible
		visible := mat.NewDense(height, width, nil)
		visible.Sub(world, Monotonic(world))
		// normalize that to 1s and 0s, indicating each visible tree
		visible.Apply(Normalize, visible)
		// add it to the highest points recorded so far
		visibleTotal.Add(visibleTotal, visible)
		// rotate the world and the highest points
		Rotate(world)
		Rotate(visibleTotal)
	}

	// set the edges to 1.0
	ones := make([]float64, width)
	for i := 0; i < width; i += 1 {
		ones[i] = 1.0
	}
	for range []int{1, 2, 3, 4} {
		visibleTotal.SetRow(0, ones)
		Rotate(visibleTotal)
	}

	// reset each non-zero value in the highest points matrix to 1
	visibleTotal.Apply(Normalize, visibleTotal)
	// sum the highest points, counting the visible trees
	return int(mat.Sum(visibleTotal))
}

func main_matrix() {
	world := ReadInputMatrix(os.Args[1])
	// create the minor diagonal at the right shape for rotation
	CreateMinor(world.Dims())

	fmt.Printf("Solution 1: %d\n", CountHighPoints(world))
}
