package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

const (
	RIGHT = iota
	DOWN
	LEFT
	UP
	TURN
	WALK
)

var offsets map[int]Coordinate = map[int]Coordinate{
	RIGHT: {1, 0},
	DOWN:  {0, 1},
	LEFT:  {-1, 0},
	UP:    {0, -1},
}

type Surface struct {
	Map                      [][]bool
	Top, Right, Bottom, Left *Surface
	Score                    []int // offset of row and column for scoring
	id                       int
}

func NewSurface(dim int) *Surface {
	s := &Surface{}
	s.Map = make([][]bool, dim)
	for i := 0; i < dim; i++ {
		row := make([]bool, dim)
		s.Map[i] = row
	}
	return s
}

type Coordinate struct{ x, y int }

func (c Coordinate) Add(o Coordinate) Coordinate { return Coordinate{x: c.x + o.x, y: c.y + o.y} }

type Player struct {
	Position  Coordinate
	Direction int
	Surface   *Surface
}

func (p *Player) TurnRight() {
	p.Direction += 1
	if p.Direction > UP {
		p.Direction = RIGHT
	}
}

func (p *Player) TurnLeft() {
	p.Direction -= 1
	if p.Direction < RIGHT {
		p.Direction = UP
	}
}

type Move struct {
	Type, Value int
}

func ParseMove(input []string) (Move, []string) {
	switch input[0] {
	case "R":
		return Move{Type: TURN, Value: RIGHT}, input[1:]
	case "L":
		return Move{Type: TURN, Value: LEFT}, input[1:]
	default:
		var val string
		for len(input) > 0 && input[0] != "R" && input[0] != "L" {
			val += input[0]
			input = input[1:]
		}
		num, _ := strconv.Atoi(val)
		return Move{Type: WALK, Value: num}, input
	}
}

func ReadInput(path string, test bool) ([]*Surface, []Move) {
	buf, _ := ioutil.ReadFile(path)
	chunks := strings.Split(string(buf), "\n\n")

	// expects the actual input to have been pre-processed into just chunks
	// of the cube surfaces, which will be stitched together hardcoded down below
	moveInput := strings.Split(chunks[len(chunks)-1], "")
	chunks = chunks[:len(chunks)-1]
	var moves []Move
	var move Move
	for len(moveInput) > 0 {
		move, moveInput = ParseMove(moveInput)
		moves = append(moves, move)
	}

	var ss []*Surface
	for i, chunk := range chunks {
		lines := strings.Split(chunk, "\n")
		s := NewSurface(len(lines))
		s.id = i
		for y := 0; y < len(lines); y += 1 {
			chars := strings.Split(lines[y], "")
			for x := 0; x < len(chars); x += 1 {
				if chars[x] == "." {
					s.Map[y][x] = false
				} else {
					s.Map[y][x] = true
				}
			}
		}
		ss = append(ss, s)
	}

	// connect together surfaces of puzzle input
	ss[0].Left, ss[0].Right, ss[0].Top, ss[0].Bottom, ss[0].Score = ss[1], ss[1], ss[4], ss[2], []int{0, 50}
	ss[1].Left, ss[1].Right, ss[1].Top, ss[1].Bottom, ss[1].Score = ss[0], ss[0], ss[1], ss[1], []int{0, 100}
	ss[2].Left, ss[2].Right, ss[2].Top, ss[2].Bottom, ss[2].Score = ss[2], ss[2], ss[0], ss[4], []int{50, 50}
	ss[3].Left, ss[3].Right, ss[3].Top, ss[3].Bottom, ss[3].Score = ss[4], ss[4], ss[5], ss[5], []int{100, 0}
	ss[4].Left, ss[4].Right, ss[4].Top, ss[4].Bottom, ss[4].Score = ss[3], ss[3], ss[2], ss[0], []int{100, 50}
	ss[5].Left, ss[5].Right, ss[5].Top, ss[5].Bottom, ss[5].Score = ss[5], ss[5], ss[3], ss[3], []int{150, 0}

	if test {
		// stitch together surfaces of the test input - different shape, different scoring offsets
		ss[0].Left, ss[0].Right, ss[0].Top, ss[0].Bottom, ss[0].Score = ss[0], ss[0], ss[4], ss[3], []int{0, 8}
		ss[1].Left, ss[1].Right, ss[1].Top, ss[1].Bottom, ss[1].Score = ss[3], ss[2], ss[1], ss[1], []int{4, 0}
		ss[2].Left, ss[2].Right, ss[2].Top, ss[2].Bottom, ss[2].Score = ss[1], ss[3], ss[2], ss[2], []int{4, 4}
		ss[3].Left, ss[3].Right, ss[3].Top, ss[3].Bottom, ss[3].Score = ss[2], ss[1], ss[0], ss[4], []int{4, 8}
		ss[4].Left, ss[4].Right, ss[4].Top, ss[4].Bottom, ss[4].Score = ss[5], ss[5], ss[3], ss[0], []int{8, 8}
		ss[5].Left, ss[5].Right, ss[5].Top, ss[5].Bottom, ss[5].Score = ss[4], ss[4], ss[5], ss[5], []int{8, 12}
	}
	return ss, moves
}

func MovePlayer(p Player, m Move) Player {
	switch m.Type {
	case TURN:
		switch m.Value {
		case RIGHT:
			p.TurnRight()
		case LEFT:
			p.TurnLeft()
		}
	case WALK:
		var offset Coordinate
		var newPosition Coordinate
		var newSurface *Surface
		var newDirection int
		for i := 0; i < m.Value; i += 1 {
			offset = offsets[p.Direction]
			newPosition = p.Position.Add(offset)
			newSurface = p.Surface
			newDirection = p.Direction
			if newPosition.y < 0 { // moving off surface up

				newSurface = p.Surface.Top
				newPosition.y = len(newSurface.Map) - 1
			} else if newPosition.y >= len(p.Surface.Map) { // moving off surface down
				newSurface = p.Surface.Bottom
				newPosition.y = 0
			} else if newPosition.x < 0 { // move off surface left
				newSurface = p.Surface.Left
				newPosition.x = len(newSurface.Map[0]) - 1
			} else if newPosition.x >= len(p.Surface.Map[0]) { // moving off surface right
				newSurface = p.Surface.Right
				newPosition.x = 0
			}
			if newSurface.Map[newPosition.y][newPosition.x] {
				break
			}
			p.Surface = newSurface
			p.Position = newPosition
			p.Direction = newDirection
		}
	}
	return p
}

func MovePlayerCube(p Player, m Move, ss []*Surface) Player {
	switch m.Type {
	case TURN:
		switch m.Value {
		case RIGHT:
			p.TurnRight()
		case LEFT:
			p.TurnLeft()
		}
	case WALK:
		var offset Coordinate
		var newPosition Coordinate
		var newSurface *Surface
		var newDirection int
		for i := 0; i < m.Value; i += 1 {
			offset = offsets[p.Direction]
			newPosition = p.Position.Add(offset)
			newSurface = p.Surface
			newDirection = p.Direction
			if newPosition.y < 0 { // moving off surface up
				switch p.Surface.id {
				case 0:
					newSurface = ss[5]
					newPosition.x = 0
					newPosition.y = p.Position.x
					newDirection = LEFT
				case 1:
					newSurface = ss[5]
					newPosition.y = len(newSurface.Map) - 1
				case 2:
					newSurface = ss[0]
					newPosition.y = len(newSurface.Map) - 1
				case 3:
					newSurface = ss[2]
					newPosition.x = 0
					newPosition.y = p.Position.x
					newDirection = LEFT
				case 4:
					newSurface = ss[2]
					newPosition.y = len(newSurface.Map) - 1
				case 5:
					newSurface = ss[3]
					newPosition.y = len(newSurface.Map) - 1
				}
			} else if newPosition.y >= len(p.Surface.Map) { // moving off surface down
				switch p.Surface.id {
				case 0:
					newSurface = ss[2]
					newPosition.y = 0
				case 1:
					newSurface = ss[2]
					newPosition.x = len(newSurface.Map[0]) - 1 // sus?
					newPosition.y = p.Position.x
					newDirection = LEFT
				case 2:
					newSurface = ss[4]
					newPosition.y = 0
				case 3:
					newSurface = ss[5]
					newPosition.y = 0
				case 4:
					newSurface = ss[5]
					newPosition.x = len(newSurface.Map[0]) - 1 // sus?
					newPosition.y = p.Position.x
					newDirection = LEFT
				case 5:
					newSurface = ss[1]
					newPosition.y = 0
				}
			} else if newPosition.x < 0 { // move off surface left
				switch p.Surface.id {
				case 0:
					newSurface = ss[3]
					newPosition.x = 0
					newPosition.y = len(newSurface.Map) - 1 - p.Position.y // sus?
					newDirection = RIGHT
				case 1:
					newSurface = ss[0]
					newPosition.x = len(newSurface.Map[0]) - 1
				case 2:
					newSurface = ss[3]
					newPosition.x = p.Position.y
					newPosition.y = 0
					newDirection = DOWN
				case 3:
					newSurface = ss[0]
					newPosition.x = 0
					newPosition.y = len(newSurface.Map) - 1 - p.Position.y // sus?
					newDirection = RIGHT
				case 4:
					newSurface = ss[3]
					newPosition.x = len(newSurface.Map[0]) - 1
				case 5:
					newSurface = ss[0]
					newPosition.x = p.Position.y
					newPosition.y = 0
					newDirection = DOWN
				}
			} else if newPosition.x >= len(p.Surface.Map[0]) { // moving off surface right
				switch p.Surface.id {
				case 0:
					newSurface = ss[1]
					newPosition.x = 0
				case 1:
					newSurface = ss[4]
					newPosition.x = len(newSurface.Map[0]) - 1
					newPosition.y = len(newSurface.Map) - 1 - p.Position.y
					newDirection = LEFT
				case 2:
					newSurface = ss[1]
					newPosition.x = p.Position.y
					newPosition.y = len(newSurface.Map) - 1
					newDirection = UP
				case 3:
					newSurface = ss[4]
					newPosition.x = 0
				case 4:
					newSurface = ss[1]
					newPosition.x = len(newSurface.Map[0]) - 1
					newPosition.y = len(newSurface.Map) - 1 - p.Position.y
					newDirection = LEFT
				case 5:
					newSurface = ss[4]
					newPosition.x = p.Position.y
					newPosition.y = len(newSurface.Map) - 1
					newDirection = UP
				}
			}
			if newSurface.Map[newPosition.y][newPosition.x] {
				break
			}
			p.Surface = newSurface
			p.Position = newPosition
			p.Direction = newDirection
		}
	}
	return p
}

func MovePlayerCubeTest(p Player, m Move, ss []*Surface) Player {
	switch m.Type {
	case TURN:
		switch m.Value {
		case RIGHT:
			p.TurnRight()
		case LEFT:
			p.TurnLeft()
		}
	case WALK:
		var offset Coordinate
		var newPosition Coordinate
		var newSurface *Surface
		var newDirection int
		for i := 0; i < m.Value; i += 1 {
			offset = offsets[p.Direction]
			newPosition = p.Position.Add(offset)
			newSurface = p.Surface
			newDirection = p.Direction
			if newPosition.y < 0 { // moving off surface up
				switch p.Surface.id {
				case 0:
					newSurface = ss[1]
					newPosition.x = len(newSurface.Map[0]) - 1 - p.Position.x
					newPosition.y = 0
					newDirection = DOWN
				case 1:
					newSurface = ss[0]
					newPosition.x = len(newSurface.Map[0]) - 1 - p.Position.x
					newPosition.y = 0
					newDirection = DOWN
				case 2:
					newSurface = ss[0]
					newPosition.x = 0
					newPosition.y = p.Position.x
					newDirection = RIGHT
				case 3:
					newSurface = ss[0]
					newPosition.y = len(newSurface.Map) - 1
				case 4:
					newSurface = ss[3]
					newPosition.y = len(newSurface.Map) - 1
				case 5:
					newSurface = ss[3]
					newPosition.x = len(newSurface.Map) - 1
					newPosition.y = p.Position.x
					newDirection = LEFT
				}
			} else if newPosition.y >= len(p.Surface.Map) { // moving off surface down
				switch p.Surface.id {
				case 0:
					newSurface = ss[3]
					newPosition.y = 0
				case 1:
					newSurface = ss[4]
					newPosition.x = len(newSurface.Map[0]) - 1 - p.Position.x
					newPosition.y = len(newSurface.Map) - 1
					newDirection = UP
				case 2:
					newSurface = ss[4]
					newPosition.x = 0
					newPosition.y = p.Position.x
					newDirection = RIGHT
				case 3:
					newSurface = ss[4]
					newPosition.y = 0
				case 4:
					newSurface = ss[1]
					newPosition.x = len(newSurface.Map[0]) - 1 - p.Position.x
					newPosition.y = len(newSurface.Map) - 1
					newDirection = UP
				case 5:
					newSurface = ss[1]
					newPosition.x = 0
					newPosition.y = p.Position.x
					newDirection = LEFT
				}
			} else if newPosition.x < 0 { // move off surface left
				switch p.Surface.id {
				case 0:
					newSurface = ss[2]
					newPosition.x = p.Position.y
					newPosition.y = 0
					newDirection = DOWN
				case 1:
					newSurface = ss[5]
					newPosition.x = len(newSurface.Map[0]) - 1
					newPosition.y = len(newSurface.Map) - 1 - p.Position.x
					newDirection = UP
				case 2:
					newSurface = ss[1]
					newPosition.x = len(newSurface.Map[0]) - 1
				case 3:
					newSurface = ss[2]
					newPosition.x = len(newSurface.Map[0]) - 1
				case 4:
					newSurface = ss[2]
					newPosition.x = len(newSurface.Map) - 1 - p.Position.y
					newPosition.y = len(newSurface.Map) - 1
					newDirection = UP
				case 5:
					newSurface = ss[4]
					newPosition.x = len(newSurface.Map) - 1
				}
			} else if newPosition.x >= len(p.Surface.Map[0]) { // moving off surface right
				switch p.Surface.id {
				case 0:
					newSurface = ss[5]
					newPosition.x = len(newSurface.Map[0]) - 1
					newPosition.y = len(newSurface.Map) - 1 - p.Position.y
					newDirection = LEFT
				case 1:
					newSurface = ss[2]
					newPosition.x = 0
				case 2:
					newSurface = ss[3]
					newPosition.x = 0
				case 3:
					newSurface = ss[5]
					newPosition.x = len(newSurface.Map[0]) - 1 - p.Position.y
					newPosition.y = 0
					newDirection = DOWN
				case 4:
					newSurface = ss[5]
					newPosition.x = 0
				case 5:
					newSurface = ss[0]
					newPosition.x = len(newSurface.Map[0]) - 1
					newPosition.y = len(newSurface.Map) - 1 - p.Position.y
					newDirection = LEFT
				}
			}
			if newSurface.Map[newPosition.y][newPosition.x] {
				break
			}
			p.Surface = newSurface
			p.Position = newPosition
			p.Direction = newDirection
		}
	}
	return p
}

func Score(player Player) int {
	row := player.Position.y + 1 + player.Surface.Score[0]
	column := player.Position.x + 1 + player.Surface.Score[1]
	return 1000*row + 4*column + player.Direction
}

func main() {
	test := false
	surfaces, moves := ReadInput(os.Args[1], test)

	player := Player{Position: Coordinate{0, 0}, Surface: surfaces[0], Direction: RIGHT}
	for _, move := range moves {
		player = MovePlayer(player, move)
	}
	fmt.Printf("Solution 1: %d\n", Score(player))

	player = Player{Position: Coordinate{0, 0}, Surface: surfaces[0], Direction: RIGHT}
	for _, move := range moves {
		player = MovePlayerCube(player, move, surfaces)
	}
	fmt.Printf("Solution 2: %d\n", Score(player))
}
