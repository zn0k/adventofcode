package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

const (
	ROCK     = 1
	PAPER    = 2
	SCISSORS = 3

	LOSE = 0
	DRAW = 3
	WIN  = 6

	MUST_LOSE = 1
	MUST_DRAW = 2
	MUST_WIN  = 3
)

type Game struct {
	You      int
	Opponent int
}

type Games []Game

// calculate the shape that beats the opponent
func (g *Game) Win() int {
	result := g.Opponent + 1
	if result > SCISSORS {
		result = ROCK
	}
	return result
}

// calculate the shape that loses to the opponent
func (g *Game) Lose() int {
	result := g.Opponent - 1
	if result < ROCK {
		result = SCISSORS
	}
	return result
}

// calculate the shape that draws with the opponent
func (g *Game) Draw() int {
	return g.Opponent
}

func (g *Game) Part1() int {
	switch g.You {
	case g.Lose():
		return g.You + LOSE
	case g.Draw():
		return g.You + DRAW
	default: // must be a win
		return g.You + WIN
	}
}

func (g *Game) Part2() int {
	switch g.You {
	case MUST_LOSE:
		return g.Lose() + LOSE
	case MUST_DRAW:
		return g.Draw() + DRAW
	default: // must win
		return g.Win() + WIN
	}
}

func ReadInput(path string) Games {
	f, err := os.Open(path)
	if err != nil {
		panic(fmt.Sprintf("unable to open '%s' for reading", path))
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)

	var games Games
	for scanner.Scan() {
		fields := strings.Fields(scanner.Text())

		game := Game{}
		switch fields[0] {
		case "A":
			game.Opponent = ROCK
		case "B":
			game.Opponent = PAPER
		case "C":
			game.Opponent = SCISSORS
		default:
			panic(fmt.Sprintf("invalid opponent move '%s'", fields[0]))
		}

		switch fields[1] {
		case "X":
			game.You = ROCK
		case "Y":
			game.You = PAPER
		case "Z":
			game.You = SCISSORS
		default:
			panic(fmt.Sprintf("invalid opponent move '%s'", fields[0]))
		}

		games = append(games, game)
	}

	return games
}

func main() {
	games := ReadInput(os.Args[1])

	score := 0
	for _, game := range games {
		score += game.Part1()
	}

	fmt.Printf("Solution 1: %d\n", score)

	score = 0
	for _, game := range games {
		score += game.Part2()
	}

	fmt.Printf("Solution 2: %d\n", score)
}
