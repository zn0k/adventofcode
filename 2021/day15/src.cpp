#include <fstream>
#include <iostream>
#include <vector>
#include <queue>
#include <map>

struct Point {
    int x;
    int y;
    Point(int x, int y) : x(x), y(y) {}
};

struct PointQueueItem {
    Point point;
    int weight;
    PointQueueItem(Point point, int weight) : point(point), weight(weight) {}
};

struct ComparePointQueueItem {
    bool operator() (PointQueueItem const &lhs, PointQueueItem const &rhs) {
        return lhs.weight > rhs.weight;
    }
};

void print_board(std::vector< std::vector<int> > board) {
    for (int y = 0; y < board.size(); y++) {
        for (int x = 0; x < board[y].size(); x++) {
            std::cout << board[y].at(x);
        }
        std::cout << std::endl;
    }
}

int get_path(std::vector< std::vector<int> > board) {
    std::priority_queue<PointQueueItem, std::vector<PointQueueItem>, ComparePointQueueItem> queue;
    std::map<Point, int> cost_so_far;
    std::map<Point, Point> came_from;

    int height = board.size();
    int width = board[0].size();

    Point start = Point(0, 0);
    cost_so_far[start] = 0;
    came_from[start] = start;

    Point goal = Point(width - 1, height - 1);

    std::vector<Point> offsets(4, Point(0, 0));
    offsets[0].x = 0;
    offsets[0].y = -1;
    offsets[1].x = 0;
    offsets[1].y = 1;
    offsets[2].x = 0;
    offsets[2].y = 1;
    offsets[3].x = -1;
    offsets[3].y = 0;

    while (!queue.empty()) {
        PointQueueItem current = queue.top();
        queue.pop();
        if (current.point.x == goal.x && current.point.y == goal.y) {
            return cost_so_far[current.point];
        }
        for(int i = 0; i < offsets.size(); i++) {
            int next_x = current.point.x + offsets[i].x;
            int next_y = current.point.y + offsets[i].y;
            if (next_x < 0 || next_x >= width || next_y < 0  || next_y >= height) {
                continue;
            }
            Point next(next_x, next_y);
            int new_cost = cost_so_far[current.point] + board[next_y].at(next_x);
            if (cost_so_far.count(next) == 0 || new_cost < cost_so_far[next]) {
                cost_so_far[next] = new_cost;
                PointQueueItem item = PointQueueItem(next, new_cost);
                queue.push(item);
                came_from[next] = current.point;
            }
        }
    }
}

int main() {
    std::ifstream in("input_test.txt");
    std::string line;
    std::getline(in, line);
    int width = line.length();
    int height = line.length();
    in.seekg(0);

    std::vector< std::vector<int> > board(height, std::vector<int>(width));
    int line_counter = 0;
    while(std::getline(in, line)) {
        for (int i = 0; i < line.length(); i++) {
            char c = line[i];
            board[line_counter].at(i) = c - '0';
        };
        line_counter++;
    };
    in.close();

    print_board(board);

    int result = get_path(board);

    std::cout << result << std::endl;
}