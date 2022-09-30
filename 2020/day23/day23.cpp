#include <iostream>
#include <vector>

// single-linked circular list of cups
struct Cup {
    int label = 0;
    Cup *next = 0;
};

void buildGame(std::vector<int> &input, int maxLabel, std::vector<Cup *> &cups, int pad=0) {
    // make the cups vector big enough to hold 0..maxLabel, plus the padding
    cups.resize(maxLabel + 1 + pad);
    // keep track of the label of the last cup added
    // if we're not padding, it's just the last label in the input
    int lastLabel = input.at(input.size() - 1);
    // create the first cup and store it, and keep a reference to it
    Cup *previous = new Cup;
    previous->label = input.at(0);
    cups.at(input.at(0)) = previous;
    // loop through the input and create new cups
    int cupCounter = 1;    
    for (int i = 1; i < input.size(); i++) {
        // create a new cup
        Cup *current = new Cup;
        current->label = input.at(i);
        // point the previous cup to this one
        previous->next = current;
        // store pointer to the new cup in the vector
        cups.at(input.at(i)) = current;
        // update the label of the last added up
        // forward
        previous = current;
        // keep counting the number of cups in the game
        cupCounter += 1;
    }
    if (pad > 0) {
        // when padding, just keep increasing the largest label
        lastLabel = maxLabel;
        // pad as necessary
        while (cupCounter < pad) {
            // increase the label by one
            lastLabel += 1;
            Cup *current = new Cup;
            current->label = lastLabel;
            // point the previous cup to this one
            previous->next = current;
            // store pointer in the vector
            cups.at(lastLabel) = current;
            // forward
            previous = current;
            // keep counting how many cups have been added
            cupCounter += 1;
        }
    } 
    // point the last cup back to the first for a circular data structure
    cups.at(lastLabel)->next = cups.at(input.at(0));
}

void printMove(std::vector<Cup *> &cups, int move, int currentLabel, int pick1, int pick2, int pick3, int destination) {
    std::cout << "-- move " << move << " --" << std::endl << "cups: (";
    std::cout << currentLabel << ") ";
    Cup *current = cups.at(currentLabel);
    while (current->next->label != currentLabel) {
        std::cout << current->next->label << " ";
        current = current->next;
    }
    std::cout << std::endl << "pick up: " << pick1 << ", " << pick2 << ", " << pick3 << std::endl;
    std::cout << "destination: " << destination << std::endl << std::endl;  
}

void playGame(std::vector<Cup *> &cups, int startLabel, int rounds, int minLabel, int maxLabel) {
    int currentLabel = startLabel;
    // get the starting cup
    Cup *currentCup = cups.at(currentLabel);
    // loop through the rounds
    for (int round = 0; round < rounds; round++) {
        // get the three cups that will be moved
        Cup *firstToMove = currentCup->next;
        Cup *secondToMove = firstToMove->next;
        Cup *thirdToMove = secondToMove->next;
        // find the destination index
        // default is current label minus 1
        int destinationLabel = currentCup->label - 1;
        // if this goes below the smallest value label, wrap around
        if (destinationLabel < minLabel) {
            destinationLabel = maxLabel;
        }
        // keep subtracting one while the destination label was picked up
        while (destinationLabel == firstToMove->label
              || destinationLabel == secondToMove->label
              || destinationLabel == thirdToMove->label) {
            destinationLabel -= 1;
            // if this goes below the smallest value label, wrap around
            if (destinationLabel < minLabel) {
                destinationLabel = maxLabel;
            }
        }
        // uncomment below to debug moves
        // printMove(cups, round + 1, currentCup->label, firstToMove->label, secondToMove->label, thirdToMove->label, destinationLabel);
        
        // get the destination cup
        Cup *destinationCup = cups.at(destinationLabel);
        // connect the current cup to the one after the slice that is being moved
        currentCup->next = thirdToMove->next;
        // point the third cup to move to what the destination cup currently points at
        thirdToMove->next = destinationCup->next;
        // point the destination cup to the first cup to move
        destinationCup->next = firstToMove;

        // move clockwise
        currentCup = currentCup->next;
    }
}

void splitInput(int input, std::vector<int> &digits) {
    // hack off the last digit and add it to the vector
    while (input > 0) {
        int digit = input % 10;
        digits.push_back(digit);
        input /= 10;
    }
    // reverse the vector
    int totalDigits = digits.size();
    for (int i = 0; i < totalDigits / 2; i++) {
        int temp = digits.at(i);
        digits.at(i) = digits.at(totalDigits - i - 1);
        digits.at(totalDigits - i - 1) = temp;
    }
}

int main(int argc, char* argv[]) {
    // split the input 
    int seed = 157623984;
    std::vector<int> input;

    splitInput(seed, input);

    // determine the label of the starting cup
    int start = input.at(0);

    // determine the min and max
    int min = 9;
    int max = 1;
    for (int i = 0; i < input.size(); i++) {
        if (input.at(i) > max) {
            max = input.at(i);
        }
        if (input.at(i) < min) {
            min = input.at(i);
        }
    }

    // vector holding the memory addresses of cups
    // for fast random access to a cup with a given label
    std::vector<Cup *> cups;

    // answer 1, play 100 rounds
    buildGame(input, max, cups);
    playGame(cups, start, 100, min, max);
    std::cout << "Answer 1: ";
    // starting at the cup with label 1, print the next cup's label
    // end when looped back to cup with label 1
    Cup *cup = cups.at(1);
    while (cup->next->label != 1) {
        std::cout << cup->next->label;
        cup = cup->next;
    }
    std::cout << std::endl;
    
    // answer 2, pad to a million cups and play 10 million rounds
    buildGame(input, max, cups, 1000000);
    playGame(cups, start, 10000000, min, max);
    std::cout << "Answer 2: ";
    // get the two cups after the cups with label 1, and multiply their labels
    cup = cups.at(1);
    std::cout << "clockwise of cup 1: " << cup->next->label << std::endl;
    std::cout << "clockwise of cup 1 plus 1: " << cup->next->next->label << std::endl;
    long long answer2 = cup->next->label * cup->next->next->label;
    std::cout << answer2 << std::endl;
}