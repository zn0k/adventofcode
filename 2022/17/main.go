package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

const (
	LEFT  = "<"
	RIGHT = ">"
)

type Jet struct {
	pattern []string
	index   int
}

func NewJet(pattern string) *Jet {
	j := &Jet{index: 0}
	j.pattern = strings.Split(pattern, "")
	return j
}

func (j *Jet) Next() string {
	if j.index >= len(j.pattern) {
		j.index = 0
	}
	char := j.pattern[j.index]
	j.index += 1
	return char
}

// pieces are just integers with bits 0-7 set based on the shapes
// why an int64? fmt.ForamtInt wants that, so this makes printing easier
// plus, should be faster on arm64s
type Piece []int64

func NewPiece(input string) Piece {
	lines := strings.Split(input, "\n")
	p := make(Piece, len(lines))
	for i := len(lines) - 1; i >= 0; i -= 1 {
		row := int64(0)
		for j, char := range lines[i] {
			if char == '#' {
				row |= (1 << j)
			}
		}
		p[len(p)-i-1] = row
	}
	return p
}

func (p Piece) String() string {
	var out bytes.Buffer
	for i := 0; i < len(p); i += 1 {
		pattern := fmt.Sprintf("%07s", strconv.FormatInt(p[i], 2))
		out.WriteString(strings.ReplaceAll(strings.ReplaceAll(pattern, "1", "#"), "0", "."))
		out.WriteString("\n")
	}
	return out.String()
}

func (p Piece) ShiftLeft() Piece {
	moved := make(Piece, len(p))
	copy(moved, p)
	for i := 0; i < len(moved); i += 1 {
		moved[i] >>= 1
	}
	return moved
}

func (p Piece) ShiftRight() Piece {
	moved := make(Piece, len(p))
	copy(moved, p)
	for i := 0; i < len(moved); i += 1 {
		moved[i] <<= 1
	}
	return moved
}

func (p Piece) InColumn(column int) bool {
	for i := 0; i < len(p); i += 1 {
		var n int64 = 1 << int64(column)
		n &= p[i]
		if n != 0 {
			return true
		}
	}
	return false
}

func (p Piece) Collision(other Piece) bool {
	for i := 0; i < len(p); i += 1 {
		if p[i]&other[i] != 0 {
			return true
		}
	}
	return false
}

// moves a piece left, is possible. takes another piece,
// representing the surrounding space
func (p Piece) Move(other Piece, direction string) Piece {
	// check if piece is up against wall it's moving towards
	// if not, move it
	var moved Piece
	switch direction {
	case LEFT:
		if p.InColumn(0) { // can't move further left
			return p
		}
		moved = p.ShiftLeft()
	case RIGHT:
		if p.InColumn(6) { // can't move further right
			return p
		}
		moved = p.ShiftRight()
	default: // should never get here
		moved = p
	}
	// check moved piece for collisions with its surroundings
	// if any bits are set in both, the piece can't move
	if moved.Collision(other) {
		return p
	}

	return moved
}

func (p Piece) Merge(other Piece) Piece {
	combined := make(Piece, len(p))
	for i := 0; i < len(p); i += 1 {
		combined[i] = p[i] | other[i]
	}
	return combined
}

type PieceGenerator struct {
	pieces []Piece
	index  int
}

func NewPieceGenerator(pieces []Piece) *PieceGenerator {
	p := &PieceGenerator{pieces: pieces}
	return p
}

func (p *PieceGenerator) Next() Piece {
	if p.index >= len(p.pieces) {
		p.index = 0
	}
	piece := p.pieces[p.index]
	result := make(Piece, len(piece))
	copy(result, piece)
	p.index += 1
	return result
}

// chamber will represent the space flipped vertically
type Chamber struct {
	board Piece
	rocks int
	jet   *Jet
}

func NewChamber(j *Jet) *Chamber {
	c := &Chamber{rocks: 0, jet: j}
	c.board = make(Piece, 0)
	return c
}

// trim empty lines from the bottom
func (c *Chamber) Trim() {
	var i int
	for i = len(c.board) - 1; i >= 0; i -= 1 {
		if c.board[i] > 0 {
			break
		}
	}
	c.board = c.board[:i+1]
}

func (c *Chamber) AddPiece(p Piece) {
	// ensure board is at least 4 units tall so the tallest piece can fit
	for len(c.board) < 4 {
		c.board = append(c.board, 0)
	}
	// the piece spawns three lines from the top
	// therefore it's always in free space and will fall three times
	// and be moved by the jet three times. do the jet movements
	empty := make(Piece, len(p))
	for i := 0; i < 3; i += 1 {
		p = p.Move(empty, c.jet.Next())
	}

	var board_line int
	var board Piece
	for board_line = len(c.board) - 1; board_line >= 0; board_line -= 1 {
		dropped := p.Move(empty, c.jet.Next()) // move the next piece
		// assemble lines from the board
		board = make(Piece, 0)
		for j := board_line; j < len(c.board); j += 1 {
			board = append(board, c.board[j])
		}
		for len(board) < len(p) {
			board = append(board, 0)
		}
		if dropped.Collision(board) {
			break
		}
		p = dropped
	}

	combined := p.Merge(board)
	for len(c.board) < board_line+len(combined) {
		c.board = append(c.board, 0)
	}
	for i := board_line; i < len(c.board); i += 1 {
		c.board[i] = combined[i-board_line]
	}
}

func (c *Chamber) String() string {
	return c.board.String()
}

func ReadInput(input_path, piece_path string) (*Jet, *PieceGenerator) {
	buf, _ := ioutil.ReadFile(input_path)
	j := NewJet(string(buf))

	buf, _ = ioutil.ReadFile(piece_path)
	var pieces []Piece
	for _, shape := range strings.Split(string(buf), "\n\n") {
		pieces = append(pieces, NewPiece(shape))
	}
	g := NewPieceGenerator(pieces)

	return j, g
}

func main() {
	jet, pieces := ReadInput(os.Args[1], "pieces.txt")
	board := NewChamber(jet)

	board.AddPiece(pieces.Next())
	fmt.Println(board)
}
