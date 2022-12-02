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

type Shape int

type Game struct {
	You      Shape
	Opponent Shape
}

type Games []Game

func (g *Game) Part1() int {
	score := LOSE
	if g.You == g.Opponent {
		score = DRAW
	}
	if (g.You == ROCK && g.Opponent == SCISSORS) ||
		(g.You == SCISSORS && g.Opponent == PAPER) ||
		(g.You == PAPER && g.Opponent == ROCK) {
		score = WIN
	}
	return int(g.You) + score
}

func (g *Game) Part2() int {
	switch g.Opponent {
	case ROCK:
		switch g.You {
		case MUST_LOSE:
			return SCISSORS + LOSE
		case MUST_DRAW:
			return ROCK + DRAW
		default: // MUST_WIN
			return PAPER + WIN
		}
	case PAPER:
		switch g.You {
		case MUST_LOSE:
			return ROCK + LOSE
		case MUST_DRAW:
			return PAPER + DRAW
		default: // MUST_WIN
			return SCISSORS + WIN
		}
	default: // SCISSORS
		switch g.You {
		case MUST_LOSE:
			return PAPER + LOSE
		case MUST_DRAW:
			return SCISSORS + DRAW
		default: // MUST_WIN
			return ROCK + WIN
		}
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
