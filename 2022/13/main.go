package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

// alright, let's build a basic lexer/parser

// first, tokens. we don't need many. tis a simple grammar
type TokenType string

const (
	EOF      = "EOF"
	INT      = "INT"
	COMMA    = ","
	LBRACKET = "["
	RBRACKET = "]"
)

type Token struct {
	Type    TokenType
	Literal string
}

// now, the lexer, which will emit a string of tokens
type Lexer struct {
	input        string
	position     int  // current position in input (current char)
	readPosition int  // current reading position in input (after current char)
	ch           byte // current char
}

func NewLexer(input string) *Lexer {
	l := &Lexer{input: input}
	l.readChar()
	return l
}

func (l *Lexer) readChar() {
	if l.readPosition >= len(l.input) {
		l.ch = 0
	} else {
		l.ch = l.input[l.readPosition]
	}
	l.position = l.readPosition
	l.readPosition += 1
}

func isDigit(ch byte) bool {
	return '0' <= ch && ch <= '9'
}

func (l *Lexer) readNumber() string {
	position := l.position
	for isDigit(l.ch) {
		l.readChar()
	}
	return l.input[position:l.position]
}

func (l *Lexer) NextToken() Token {
	var tok Token
	switch l.ch {
	case '[':
		tok = Token{Type: LBRACKET, Literal: string(l.ch)}
		l.readChar()
	case ']':
		tok = Token{Type: RBRACKET, Literal: string(l.ch)}
		l.readChar()
	case ',':
		tok = Token{Type: COMMA, Literal: string(l.ch)}
		l.readChar()
	case 0:
		tok = Token{Type: EOF, Literal: ""}
		l.readChar()
	default: // must be an integer
		tok = Token{Type: INT, Literal: l.readNumber()}
	}
	//l.readChar()
	return tok
}

// the AST objects we can represent - just integers and lists
type Element interface {
	element()
	String() string
}

type Integer struct {
	Value int64
}

func (i *Integer) element() {}
func (i *Integer) String() string {
	return fmt.Sprintf("%d", i.Value)
}

type List struct {
	Elements []Element
}

func (l *List) element() {}
func (l *List) String() string {
	out := "["
	for _, e := range l.Elements {
		out += e.String() + ", "
	}
	return out + "]"
}

// the parser
type Parser struct {
	l         *Lexer
	curToken  Token
	peekToken Token
}

func NewParser(l *Lexer) *Parser {
	p := &Parser{l: l}
	p.nextToken()
	p.nextToken()
	return p
}

func (p *Parser) nextToken() {
	p.curToken = p.peekToken
	p.peekToken = p.l.NextToken()
	fmt.Printf("Forwarded to token %s\n", p.curToken.Literal)
}

func (p *Parser) Parse() Element {
	p.nextToken()
	list := &List{}
	list.Elements = make([]Element, 0)

	for p.curToken.Type != EOF {
		if p.peekToken.Type == RBRACKET {
			//p.nextToken()
			return list
		}
		for p.peekToken.Type == COMMA {
			if p.curToken.Type == LBRACKET {
				p.nextToken()
				e := p.Parse()
				list.Elements = append(list.Elements, e)
			}
			if p.curToken.Type == INT {
				i, _ := strconv.ParseInt(p.curToken.Literal, 10, 64)
				list.Elements = append(list.Elements, &Integer{Value: i})
				p.nextToken()
			}
			p.nextToken()
		}
		p.nextToken()
	}
	return list
}

func ReadInput(path string) [][]Element {
	buf, err := os.ReadFile(path)
	if err != nil {
		panic(fmt.Sprintf("unable to read from %s", path))
	}

	var pairs [][]Element
	for _, chunk := range strings.Split(string(buf), "\n\n") {
		var pair []Element
		for _, line := range strings.Split(chunk, "\n") {
			l := NewLexer(strings.Trim(line, "\n"))
			p := NewParser(l)
			e := p.Parse()
			pair = append(pair, e)
		}
		pairs = append(pairs, pair)
	}
	return pairs
}

func main() {
	pairs := ReadInput(os.Args[1])
	for _, pair := range pairs {
		fmt.Println(pair[0])
		fmt.Println(pair[1])
	}
}
