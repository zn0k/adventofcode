package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"strings"
	"unicode/utf8"
)

func Snafu2Int(in string) int64 {
	in = Reverse(in)
	result := int64(0)
	for i, c := range in {
		d := int64(0)
		switch c {
		case '2':
			d = 2
		case '1':
			d = 1
		case '0':
			d = 0
		case '-':
			d = -1
		case '=':
			d = -2
		default:
			panic(fmt.Sprintf("invalid digit %s in snafu number", string(c)))
		}
		d = int64(math.Pow(5, float64(i))) * d
		result += d
	}
	return result
}

func Int2Snafu(i int64) string {
	digits := make([]string, 0)
	for i != 0 {
		rem := ((i + 2) % 5) - 2
		switch rem {
		case -2:
			digits = append(digits, "=")
		case -1:
			digits = append(digits, "-")
		case 0:
			digits = append(digits, "0")
		case 1:
			digits = append(digits, "1")
		case 2:
			digits = append(digits, "2")
		default:
			panic(fmt.Sprintf("invalid remainder %d", rem))
		}
		i = (i + 2) / 5
	}
	return Reverse(strings.Join(digits, ""))
}

func Reverse(s string) string {
	size := len(s)
	buf := make([]byte, size)
	for start := 0; start < size; {
		r, n := utf8.DecodeRuneInString(s[start:])
		start += n
		utf8.EncodeRune(buf[size-start:], r)
	}
	return string(buf)
}

func AddSnafuDigits(a, b string) (string, string) {
	switch a {
	case "2":
		switch b {
		case "2":
			return "-", "1"
		case "1":
			return "=", "1"
		case "0":
			return "2", ""
		case "-":
			return "1", ""
		case "=":
			return "0", ""
		}
	case "1":
		switch b {
		case "2":
			return "=", "1"
		case "1":
			return "2", ""
		case "0":
			return "1", ""
		case "-":
			return "0", ""
		case "=":
			return "-", ""
		}
	case "0":
		return b, ""
	case "-":
		switch b {
		case "2":
			return "1", ""
		case "1":
			return "0", ""
		case "0":
			return "-", ""
		case "-":
			return "=", ""
		case "=":
			return "2", "-"
		}
	case "=":
		switch b {
		case "2":
			return "0", ""
		case "1":
			return "-", ""
		case "0":
			return "=", ""
		case "-":
			return "2", "-"
		case "=":
			return "1", "-"
		}
	}
	panic(fmt.Sprintf("invalid digits %s and %s being added", a, b))
}

func AddSnafu(a, b string) string {
	if a == "" {
		if b == "" {
			return ""
		} else {
			return b
		}
	}
	if b == "" {
		return a
	}

	da := strings.Split(a, "")
	db := strings.Split(b, "")
	summed, remainder := AddSnafuDigits(da[len(da)-1], db[len(db)-1])
	return AddSnafu(remainder, AddSnafu(strings.Join(da[0:len(da)-1], ""), strings.Join(db[0:len(db)-1], ""))) + summed
}

func main() {
	buf, _ := ioutil.ReadFile(os.Args[1])

	// can convert input to integer, and then convert sum back to snafu
	/*sum := int64(0)
	for _, n := range strings.Split(string(buf), "\n") {
		sum += Snafu2Int(n)
	}
	fmt.Printf("Solution 1: %s\n", Int2Snafu(sum))*/

	// but it's kinda neater to just add snafu numbers directly
	sum := ""
	for _, num := range strings.Split(string(buf), "\n") {
		sum = AddSnafu(sum, num)
	}
	fmt.Printf("Solution 1: %s\n", sum)

}
