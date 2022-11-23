package main

import (
	"fmt"
	"math"

	"gonum.org/v1/gonum/stat/combin"
)

type Coordinate struct {
	x, y, z int
}

type Moon struct {
	Position Coordinate
	Velocity Coordinate
}

func (moon *Moon) CalculateVelocity(other *Moon) {
	if moon.Position.x < other.Position.x {
		moon.Velocity.x++
		other.Velocity.x--
	} else if moon.Position.x > other.Position.x {
		moon.Velocity.x--
		other.Velocity.x++
	}

	if moon.Position.y < other.Position.y {
		moon.Velocity.y++
		other.Velocity.y--
	} else if moon.Position.y > other.Position.y {
		moon.Velocity.y--
		other.Velocity.y++
	}

	if moon.Position.z < other.Position.z {
		moon.Velocity.z++
		other.Velocity.z--
	} else if moon.Position.z > other.Position.z {
		moon.Velocity.z--
		other.Velocity.z++
	}
}

func (moon *Moon) Move() {
	moon.Position.x += moon.Velocity.x
	moon.Position.y += moon.Velocity.y
	moon.Position.z += moon.Velocity.z
}

func (moon *Moon) Energy() int {
	pot := int(math.Abs(float64(moon.Position.x)) + math.Abs(float64(moon.Position.y)) + math.Abs(float64(moon.Position.z)))
	kin := int(math.Abs(float64(moon.Velocity.x)) + math.Abs(float64(moon.Velocity.y)) + math.Abs(float64(moon.Velocity.z)))
	return pot * kin
}

func StepForward(moons []Moon) {
	combinations := combin.Combinations(len(moons), 2)
	for _, pair := range combinations {
		moons[pair[0]].CalculateVelocity(&moons[pair[1]])
	}
	for i := 0; i < len(moons); i++ {
		moons[i].Move()
	}
}

func GetSystemEnergy(moons []Moon) int {
	total := 0
	for i := 0; i < len(moons); i++ {
		total += moons[i].Energy()
	}
	return total
}

type State struct {
	pos1, pos2, pos3, pos4 int // position axis values
	vel1, vel2, vel3, vel4 int // velocity axis values
}

func NumberOfStepsToRepeat(moons []Moon) int64 {
	// keep a history of states for each axis
	states_x := make(map[State]bool)
	states_y := make(map[State]bool)
	states_z := make(map[State]bool)

	for {
		// calculate the current state
		state_x := State{
			moons[0].Position.x, moons[1].Position.x, moons[2].Position.x, moons[3].Position.x,
			moons[0].Velocity.x, moons[1].Velocity.x, moons[2].Velocity.x, moons[3].Velocity.x,
		}
		state_y := State{
			moons[0].Position.y, moons[1].Position.y, moons[2].Position.y, moons[3].Position.y,
			moons[0].Velocity.y, moons[1].Velocity.y, moons[2].Velocity.y, moons[3].Velocity.y,
		}
		state_z := State{
			moons[0].Position.z, moons[1].Position.z, moons[2].Position.z, moons[3].Position.z,
			moons[0].Velocity.z, moons[1].Velocity.z, moons[2].Velocity.z, moons[3].Velocity.z,
		}

		// check if these axis states have been seen before
		_, x_seen := states_x[state_x]
		_, y_seen := states_y[state_y]
		_, z_seen := states_z[state_z]

		if x_seen && y_seen && z_seen {
			// all three axis states are a reoccurence, break out of the loop
			break
		}

		// at least one axis state is new, add them all to the seen states
		// since it's a map, if a state was seen before, this doesn't change the map
		states_x[state_x] = true
		states_y[state_y] = true
		states_z[state_z] = true

		// step forward in time
		StepForward(moons)
	}

	// count the total number of states on each axis
	num_x := int64(len(states_x))
	num_y := int64(len(states_y))
	num_z := int64(len(states_z))

	// answer is least common multiple between the axis state counts
	return lcm(num_x, lcm(num_y, num_z))
}

func lcm(x, y int64) int64 {
	var a int64 = x
	var b int64 = y
	for a > 0 {
		a, b = b%a, a
	}
	return x / b * y
}

func main() {
	moons := []Moon{
		{Position: Coordinate{-7, -1, 6}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{6, -9, -9}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{-12, 2, -7}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{4, -17, -12}, Velocity: Coordinate{0, 0, 0}},
	}

	for i := 0; i < 1000; i++ {
		StepForward(moons)
	}

	solution1 := GetSystemEnergy(moons)
	fmt.Printf("Solution 1: %d\n", solution1)

	moons = []Moon{
		{Position: Coordinate{-7, -1, 6}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{6, -9, -9}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{-12, 2, -7}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{4, -17, -12}, Velocity: Coordinate{0, 0, 0}},
	}

	solution2 := NumberOfStepsToRepeat(moons)
	fmt.Printf("Solution 2: %d\n", solution2)
}
