package main

import (
	"bytes"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

type PacketType int

const (
	_ = iota
	INTEGER
	LIST
)

type Packet struct {
	Type   PacketType
	Value  int64
	Items  []*Packet
	Marked bool
}

func (p *Packet) String() string {
	switch p.Type {
	case INTEGER:
		return fmt.Sprintf("%d", p.Value)
	case LIST:
		var out bytes.Buffer
		out.WriteString("[")
		for _, i := range p.Items {
			out.WriteString(i.String() + ", ")
		}
		out.WriteString("]")
		return out.String()
	}
	return ""
}

const (
	LT = -1
	EQ = 0
	GT = 1
)

func (l *Packet) Cmp(r *Packet) int {
	if l.Type == INTEGER && r.Type == INTEGER {
		if l.Value < r.Value {
			return LT
		}
		if l.Value > r.Value {
			return GT
		}
		return EQ
	}

	if l.Type == LIST && r.Type == LIST {
		for i := 0; i < len(l.Items) && i < len(r.Items); i += 1 {
			result := l.Items[i].Cmp(r.Items[i])
			if result != 0 {
				return result
			}
		}
		if len(l.Items) < len(r.Items) {
			return LT
		}
		if len(l.Items) > len(r.Items) {
			return GT
		}
		return EQ
	}

	if l.Type == LIST && r.Type == INTEGER {
		rl := &Packet{Type: LIST}
		rl.Items = make([]*Packet, 1)
		rl.Items[0] = r
		return l.Cmp(rl)
	}

	if l.Type == INTEGER && r.Type == LIST {
		ll := &Packet{Type: LIST}
		ll.Items = make([]*Packet, 1)
		ll.Items[0] = l
		return ll.Cmp(r)
	}

	return 0
}

// declare a type alias for a list of packets
type Packets []*Packet

// and implement sort.Interface on them, so we can sort the list
func (p Packets) Len() int {
	return len(p)
}

func (p Packets) Swap(i, j int) {
	p[i], p[j] = p[j], p[i]
}

func (p Packets) Less(i, j int) bool {
	return p[i].Cmp(p[j]) == -1
}

func isDigit(ch rune) bool { return '0' <= ch && ch <= '9' }

func parseInt(chars []rune) (*Packet, []rune) {
	i := 0
	for i = 0; i < len(chars) && isDigit(chars[i]); {
		i += 1
	}
	num, _ := strconv.ParseInt(string(chars[0:i]), 10, 64)
	packet := &Packet{Type: INTEGER, Value: num}
	chars = chars[i:]
	return packet, chars
}

func parseList(chars []rune) (*Packet, []rune) {
	chars = chars[1:]
	packet := &Packet{Type: LIST}
	packet.Items = make([]*Packet, 0)
LOOP:
	for len(chars) > 0 {
		switch chars[0] {
		case ']':
			chars = chars[1:]
			break LOOP
		case ',':
			chars = chars[1:]
		case '[':
			var child *Packet
			child, chars = parseList(chars)
			packet.Items = append(packet.Items, child)
		default:
			var child *Packet
			child, chars = parseInt(chars)
			packet.Items = append(packet.Items, child)
		}
	}
	return packet, chars
}

func ParsePacket(chars []rune) *Packet {
	packet, _ := parseList(chars)
	return packet
}

func ReadInput(path string) Packets {
	buf, err := os.ReadFile(path)
	if err != nil {
		panic(fmt.Sprintf("unable to read from %s", path))
	}

	var packets []*Packet
	for _, chunk := range strings.Split(string(buf), "\n\n") {
		lines := strings.Split(chunk, "\n")
		left := ParsePacket([]rune(lines[0]))
		right := ParsePacket([]rune(lines[1]))
		packets = append(packets, left, right)
	}
	return packets
}

func main() {
	packets := ReadInput(os.Args[1])
	sum := 0
	for i := 0; i < len(packets); i += 2 {
		result := packets[i].Cmp(packets[i+1])
		if result == -1 {
			sum += (i / 2) + 1
		}
	}
	fmt.Printf("Solution 1: %d\n", sum)

	special1 := ParsePacket([]rune("[[2]]"))
	special1.Marked = true
	special2 := ParsePacket([]rune("[[6]]"))
	special2.Marked = true
	packets = append(packets, special1, special2)
	sort.Sort(Packets(packets))
	key := 1
	for i := 0; i < len(packets); i += 1 {
		if packets[i].Marked {
			key *= (i + 1)
		}
	}
	fmt.Printf("Solution 2: %d\n", key)
}
