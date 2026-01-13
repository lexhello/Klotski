#include <iostream>
#include <string>

int main() {

    std::string input;
    
    // Read one line from stdin (blocking)
    if (!std::getline(std::cin, input)) {
        std::cerr << "No input received\n";
        return 1;
    }

    // Simulate heavy computation
    // TODO: Replace with actual complex solver logic
    int next_move = 100; // placeholder output

    // Example protocol: Python expects "MOVE:<int>"
    std::cout << "MOVE:" << next_move << std::endl;

    return 0;
}
