#include <fstream>
#include <iostream>
#include <vector>
#include <limits>

typedef std::numeric_limits< double > dbl;

int main() {
    std::ifstream in("input.txt");
    std::string line;

    unsigned long long int stack = 0;
    long penalty = 0;
    std::vector<double> scores;

    while(std::getline(in, line)) {
        stack = 3;
        for (int i = 0; i < line.length(); i++) {
            char c = line[i];
            int val = 0;
            int p = 3;
            if (c == '(' || c == '[' or c == '{' or c == '<') {
                switch (c) {
                    case '[':
                        val = 1;
                        break;
                    case '{':
                        val = 2;
                        break;
                    case '<':
                        val = 3;
                }
                stack = stack << 2;
                stack += val;
            } else {
                switch (c) {
                    case ']':
                        val = 1;
                        p = 57;
                        break;
                    case '}':
                        val = 2;
                        p = 1197;
                        break;
                    case '>':
                        val = 3;
                        p = 25137;
                }
                int last = stack & 3;
                stack = stack >> 2;
                if (last != val) {
                    penalty += p;
                    stack = 0;
                    break;
                }
            }
        }
        long score = 0;
        while (stack > 3) {
            int next = stack & 3;
            stack = stack >> 2;
            score *= 5;
            score += next + 1;
        }
        if (score != 0) {
            scores.push_back(score);
        }
    }
    std::cout << "Solution 1: " << penalty << std::endl;
    std::cout.precision(dbl::max_digits10);
    std::nth_element(scores.begin(), scores.begin() + scores.size() / 2, scores.end());
    std::cout << "Solution 2: " << scores.at(int(scores.size() / 2)) << std::endl;
}