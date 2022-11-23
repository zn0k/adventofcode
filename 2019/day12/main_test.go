package main

import (
	"testing"
)

func TestVelocity(t *testing.T) {
	ganymede := Moon{Position: Coordinate{3, 0, 0}, Velocity: Coordinate{0, 0, 0}}
	callisto := Moon{Position: Coordinate{5, 0, 0}, Velocity: Coordinate{0, 0, 0}}

	ganymede.CalculateVelocity(&callisto)

	if ganymede.Velocity.x != 1 {
		t.Errorf("ganymede's x velocity is not %d, got %d", 1, ganymede.Velocity.x)
	}
	if callisto.Velocity.x != -1 {
		t.Errorf("callisto's x velocity is not %d, got %d", -1, callisto.Velocity.x)
	}
}

func TestMove(t *testing.T) {
	europa := Moon{Position: Coordinate{1, 2, 3}, Velocity: Coordinate{-2, 0, 3}}
	europa.Move()

	expected := Moon{Position: Coordinate{-1, 2, 6}, Velocity: europa.Velocity}

	compareMoons(t, europa, expected)
}

func TestStepForward(t *testing.T) {
	moons := []Moon{
		{Position: Coordinate{-1, 0, 2}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{2, -10, -7}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{4, -8, 8}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{3, 5, -1}, Velocity: Coordinate{0, 0, 0}},
	}

	StepForward(moons)

	expectedAfter1 := []Moon{
		{Position: Coordinate{2, -1, 1}, Velocity: Coordinate{3, -1, -1}},
		{Position: Coordinate{3, -7, -4}, Velocity: Coordinate{1, 3, 3}},
		{Position: Coordinate{1, -7, 5}, Velocity: Coordinate{-3, 1, -3}},
		{Position: Coordinate{2, 2, 0}, Velocity: Coordinate{-1, -3, 1}},
	}
	for i, moon := range moons {
		compareMoons(t, moon, expectedAfter1[i])
	}

	for i := 0; i < 9; i++ {
		StepForward(moons)
	}

	expectedAfter10 := []Moon{
		{Position: Coordinate{2, 1, -3}, Velocity: Coordinate{-3, -2, 1}},
		{Position: Coordinate{1, -8, 0}, Velocity: Coordinate{-1, 1, 3}},
		{Position: Coordinate{3, -6, 1}, Velocity: Coordinate{3, 2, -3}},
		{Position: Coordinate{2, 0, 4}, Velocity: Coordinate{1, -1, -1}},
	}

	for i, moon := range moons {
		compareMoons(t, moon, expectedAfter10[i])
	}
}

func TestEnergy(t *testing.T) {
	moons := []Moon{
		{Position: Coordinate{-1, 0, 2}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{2, -10, -7}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{4, -8, 8}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{3, 5, -1}, Velocity: Coordinate{0, 0, 0}},
	}

	for i := 0; i < 10; i++ {
		StepForward(moons)
	}

	energy := GetSystemEnergy(moons)

	if energy != 179 {
		t.Errorf("system energy is not %d, got %d", 179, energy)
	}

	moons = []Moon{
		{Position: Coordinate{-8, -10, 0}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{5, 5, 10}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{2, -7, 3}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{9, -8, -3}, Velocity: Coordinate{0, 0, 0}},
	}

	for i := 0; i < 100; i++ {
		StepForward(moons)
	}

	energy = GetSystemEnergy(moons)

	if energy != 1940 {
		t.Errorf("system energy is not %d, got %d", 1940, energy)
	}

}

func compareMoons(t *testing.T, moon, expected Moon) bool {
	problem := false
	if moon.Position.x != expected.Position.x {
		t.Errorf("x coordinate is not %d, got %d", expected.Position.x, moon.Position.x)
		problem = true
	}
	if moon.Position.y != expected.Position.y {
		t.Errorf("y coordinate is not %d, got %d", expected.Position.y, moon.Position.y)
		problem = true
	}
	if moon.Position.z != expected.Position.z {
		t.Errorf("z coordinate is not %d, got %d", expected.Position.z, moon.Position.z)
		problem = true
	}

	if moon.Velocity.x != expected.Velocity.x {
		t.Errorf("x velocity is not %d, got %d", expected.Velocity.x, moon.Velocity.x)
		problem = true
	}
	if moon.Velocity.y != expected.Velocity.y {
		t.Errorf("y velocity is not %d, got %d", expected.Velocity.y, moon.Velocity.y)
		problem = true
	}
	if moon.Velocity.z != expected.Velocity.z {
		t.Errorf("z velocity is not %d, got %d", expected.Velocity.z, moon.Velocity.z)
		problem = true
	}

	return problem
}

func TestRepeat(t *testing.T) {
	moons := []Moon{
		{Position: Coordinate{-1, 0, 2}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{2, -10, -7}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{4, -8, 8}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{3, 5, -1}, Velocity: Coordinate{0, 0, 0}},
	}

	result := NumberOfStepsToRepeat(moons)

	if result != 2772 {
		t.Errorf("number of steps to repeat isn't %d, got %d", 2772, result)
	}

	moons = []Moon{
		{Position: Coordinate{-8, -10, 0}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{5, 5, 10}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{2, -7, 3}, Velocity: Coordinate{0, 0, 0}},
		{Position: Coordinate{9, -8, -3}, Velocity: Coordinate{0, 0, 0}},
	}

	result = NumberOfStepsToRepeat(moons)

	if result != 4686774924 {
		t.Errorf("number of steps to repeat isn't %d, got %d", 4686774924, result)
	}
}
