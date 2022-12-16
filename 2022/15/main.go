package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"sort"
	"strings"
)

type Coordinate struct{ x, y int64 }

func (c *Coordinate) Add(o Coordinate) Coordinate { return Coordinate{c.x + o.x, c.y + o.y} }
func (c *Coordinate) IsValid() bool               { return c.x > 0 && c.x < 4_000_000 && c.y > 0 && c.y < 4_000_000 }

type Sensor struct {
	Location, Beacon Coordinate
	Distance         int64
}

// returns true if the sensor covers a particular row
func (s *Sensor) CoversRow(row int64) bool {
	top := s.Location.Add(Coordinate{0, -s.Distance})   // top coverage
	bottom := s.Location.Add(Coordinate{0, s.Distance}) // bottom
	if top.y <= row && bottom.y >= row {
		return true
	}
	return false
}

// returns true if a point is within reach of the sensor
func (s *Sensor) CoversPoint(c Coordinate) bool {
	return ManhattanDistance(&s.Location, &c) <= s.Distance
}

// returns the range in the given row covered by the sensor
func (s *Sensor) CoveredRange(row int64) (int64, int64) {
	d := ManhattanDistance(&s.Location, &s.Beacon)
	remains := d - Abs(s.Location.y-row)
	start, end := s.Location.x-remains, s.Location.x+remains
	return start, end
}

// return the four corner points just outside the range of the sensor
func (s *Sensor) EnvelopePoints() Envelope {
	top := s.Location.Add(Coordinate{0, -s.Distance - 1})
	right := s.Location.Add(Coordinate{s.Distance + 1, 0})
	bottom := s.Location.Add(Coordinate{0, s.Distance + 1})
	left := s.Location.Add(Coordinate{-s.Distance - 1, 0})
	return Envelope{top, right, bottom, left}
}

func NewSensor(l, b Coordinate) *Sensor {
	s := &Sensor{Location: l, Beacon: b}
	s.Distance = ManhattanDistance(&l, &b)
	return s
}

type Envelope struct{ Top, Right, Bottom, Left Coordinate }

type Range struct{ Start, End int64 }

type Ranges []Range

func (r Ranges) Len() int           { return len(r) }
func (r Ranges) Swap(i, j int)      { r[i], r[j] = r[j], r[i] }
func (r Ranges) Less(i, j int) bool { return r[i].Start < r[j].Start }

// counts the fields excluded by a sorted series of ranges
func (rs Ranges) Count() int64 {
	var count int64 = 0
	var last int64 = -math.MaxInt64
	for _, r := range rs {
		if r.Start > last {
			count += (r.End - r.Start) + 1
			last = r.End
		} else if r.Start <= last && r.End > last {
			count += (r.End - last)
			last = r.End
		} else {
		}
	}
	return count
}

type Line struct{ slope, y int64 }

// calculate the intersection of two lines
func (line *Line) Intersection(other *Line) Coordinate {
	if line.slope == other.slope {
		return Coordinate{math.MaxInt64, math.MaxInt64}
	}
	x := (other.y - line.y) / (line.slope - other.slope)
	y := line.slope*x + line.y
	return Coordinate{x, y}
}

func NewLine(a, b Coordinate) Line {
	slope := (b.y - a.y) / (b.x - a.x)
	y := a.y - slope*a.x
	return Line{slope, y}
}

func Abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func ManhattanDistance(p1, p2 *Coordinate) int64 { return Abs(p1.x-p2.x) + Abs(p1.y-p2.y) }

func ReadInput(path string) []Sensor {
	buf, _ := ioutil.ReadFile(path)
	var sensors []Sensor
	var sx, sy, bx, by int64
	for _, line := range strings.Split(string(buf), "\n") {
		fmt.Sscanf(line, "Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d", &sx, &sy, &bx, &by)
		location, beacon := Coordinate{sx, sy}, Coordinate{bx, by}
		sensor := NewSensor(location, beacon)
		sensors = append(sensors, *sensor)
	}
	return sensors
}

func main() {
	sensors := ReadInput(os.Args[1])
	row := int64(2_000_000)
	ranges := make(Ranges, 0)
	beacons_in_row := make(map[Coordinate]bool) // keep track of beacons in the given row
	var descs []Line                            // lines that run diagonally descending left to right
	var ascs []Line                             // lines that run diagonally ascending right to left
	for _, sensor := range sensors {
		if sensor.Beacon.y == row { // this sensor has a beacon in that row, record that
			beacons_in_row[sensor.Beacon] = true
		}
		if sensor.CoversRow(row) { // sensor covers the row, get the range of fields it covers
			start, end := sensor.CoveredRange(row)
			ranges = append(ranges, Range{start, end})
		}
		e := sensor.EnvelopePoints() // get the corner points just outside the coverage
		// create the four lines that circumscribe the sensors, split into the two
		// sets of parallel lines
		descs = append(descs, NewLine(e.Top, e.Right), NewLine(e.Left, e.Bottom))
		ascs = append(ascs, NewLine(e.Top, e.Left), NewLine(e.Right, e.Bottom))
	}
	sort.Sort(ranges)
	fmt.Printf("Solution 1: %d\n", ranges.Count()-int64(len(beacons_in_row)))

	// find all the intersections in the relevant quadrant
	intersections := make(map[Coordinate]bool)
	for _, desc := range descs {
		for _, asc := range ascs {
			intersection := desc.Intersection(&asc)
			if intersection.IsValid() {
				intersections[intersection] = true
			}
		}
	}

	// check all possible intersections to find the one not covered by a sensor
	for intersection := range intersections {
		covered := false
		for _, sensor := range sensors {
			if sensor.CoversPoint(intersection) {
				covered = true
				break
			}
		}
		if !covered {
			fmt.Printf("Solution 2: %d\n", intersection.x*4000000+intersection.y)
		}
	}
}
