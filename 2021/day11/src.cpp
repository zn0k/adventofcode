#include <fstream>
#include <iostream>
#include <algorithm>

int width = 0;
int height = 0;

void add(int a[], int b[], size_t size) {
    for (int i = 0; i < size; i++) {
        a[i] += b[i];
    }
}

void print_board(int a[], int width, int height) {
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            std::cout << a[i * width + j];
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

void get_neighbors(int index, int n[], int width, int height) {
    int offsets[] = {index - width - 1, index - width, index - width + 1,
                     index - 1, index + 1, 
                     index + width - 1, index + width, index + width + 1};
    int offset_add[8];
    std::fill_n(offset_add, 8, index);
    add(offsets, offset_add, 8);
    int max_index = width * height;
    for (int i = 0; i < 8; i++) {
        if (offsets[i] > 0 && offsets[i] < max_index) {
            n[i] = offsets[i];
        } else {
            n[i] = 0;
        }
    }
}

int main() {
    std::ifstream in("11-100-2.in");
    std::string line;
    std::getline(in, line);
    int width = line.length();
    int height = line.length();
    in.seekg(0);

    int dumbos[width * height];
    int ones[width * height];
    std::fill_n(ones, width * height, 1);
    int zeroes[width * height];
    std::fill_n(zeroes, width * height, 0);
    int neighbors[8];
    int done[width * height];

    int lineCounter = 0;
    int index = 0;
    while(std::getline(in, line)) {
        for (int i = 0; i < line.length(); i++) {
            char c = line[i];
            int j = c - '0';
            index = lineCounter * width + i;
            dumbos[index] = j;
        }
        lineCounter += 1;
    }
    in.close();

    int total_flashes = 0;
    int step = 0;

    while(1) {
        step++;
        add(dumbos, ones, width * height);
        memcpy(done, zeroes, sizeof zeroes);
        bool flashed = true;
        while (flashed) {
            flashed = false;
            for (int i = 0; i < width * height; i++) {
                if (dumbos[i] > 9 && done[i] != 0) {
                    get_neighbors(i, neighbors, width, height);
                    for (int j = 0; j < 8; j++) {
                        if (neighbors[j] != 0) {
                            dumbos[neighbors[j]] += 1;
                        }
                    }
                    done[i] = 1;
                    flashed = true;
                    if (step < 100) { total_flashes++; }
                }
            }
        }
        int all_synced = true;
        for (int i = 0; i < width * height; i++) {
            if (done[i] == 1) { dumbos[i] = 0; }
            if (dumbos[i] != 0) { all_synced = false; }
        }
        if (all_synced) { 
            break;
        }
    }

    std::cout << "Solution 1: " << total_flashes << std::endl;
    std::cout << "Solution 2: " << step << std::endl;
}