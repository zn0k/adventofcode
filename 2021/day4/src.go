package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// custom type to represent a board
type Board struct {
	// 2-dimensional array of ints to represent the board state
	board [][]int
	// mark whether the board has been won
	won bool
}

func readLines(path string) ([]int, []Board, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, nil, err
	}
	defer file.Close()

	var draws []int
	var boards []Board
	pos := 0

	var board [][]int
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		pos += 1

		// first line is the comma separated draws
		if pos == 1 {
			for _, word := range strings.Split(line, ",") {
				draw, err := strconv.ParseInt(word, 10, 32)
				if err != nil {
					return nil, nil, err
				}
				draws = append(draws, int(draw))
			}
			continue
		}

		// second line needs to just be skipped
		if pos == 2 {
			continue
		}

		// empty lines mean board is done, so push it to the boards
		if len(line) == 0 {
			boards = append(boards, Board{board, false})
			// then reset the current board being assembled
			board = [][]int{}
			continue
		}

		// else, parse the line into integers and add them to the current board
		var boardLine []int
		for _, word := range strings.Fields(line) {
			field, err := strconv.ParseInt(word, 10, 32)
			if err != nil {
				return nil, nil, err
			}
			boardLine = append(boardLine, int(field))
		}
		board = append(board, boardLine)
	}
	// append the final board
	boards = append(boards, Board{board, false})

	return draws, boards, scanner.Err()
}

// check if a board has won
func checkBoard(board Board) bool {
	// check horizontals
	for _, line := range board.board {
		allMarked := true
		for _, val := range line {
			if val != -1 {
				allMarked = false
				break
			}
		}
		if allMarked {
			return true
		}
	}

	// check verticals
	for i := 0; i < len(board.board[0]); i++ {
		allMarked := true
		for _, line := range board.board {
			if line[i] != -1 {
				allMarked = false
				break
			}
		}
		if allMarked {
			return true
		}
	}

	return false
}

func markBoard(board Board, draw int) Board {
	for hPos, line := range board.board {
		for vPos, field := range line {
			if field == draw {
				board.board[hPos][vPos] = -1
			}
		}
	}
	return board
}

func scoreBoard(board Board, draw int) int {
	sum := 0
	for _, line := range board.board {
		for _, field := range line {
			if field != -1 {
				sum += field
			}
		}
	}
	return sum * draw
}

func main() {
	draws, boards, err := readLines(os.Args[1])
	if err != nil {
		panic(err)
	}

	var scores []int
	for _, draw := range draws {
		for i := 0; i < len(boards); i++ {
			if boards[i].won {
				continue
			}
			boards[i] = markBoard(boards[i], draw)
			if checkBoard(boards[i]) {
				boards[i].won = true
				scores = append(scores, scoreBoard(boards[i], draw))
			}
		}
	}
	fmt.Printf("Solution 1: %d\n", scores[0])
	fmt.Printf("Solution 2: %d\n", scores[len(scores)-1])
}
