#include <iostream>
#include <vector>
#include <chrono>
#include <cstdint>

class SudokuSolver {
private:
    static const int BOARD_SIZE = 9;
    static const int SQUARE_SIZE = 3;
    
    // Bit masks for each number (1-9)
    // 1 = 000000001, 2 = 000000010, 3 = 000000100, etc.
    static constexpr uint16_t MASKS[10] = {
        0,      // 0 (unused)
        1,      // 1: 000000001
        2,      // 2: 000000010
        4,      // 3: 000000100
        8,      // 4: 000001000
        16,     // 5: 000010000
        32,     // 6: 000100000
        64,     // 7: 001000000
        128,    // 8: 010000000
        256     // 9: 100000000
    };
    
    std::vector<std::vector<int>> board;
    std::vector<uint16_t> rowMasks;    // Bit masks for each row
    std::vector<uint16_t> colMasks;    // Bit masks for each column
    std::vector<uint16_t> squareMasks; // Bit masks for each 3x3 square
    
    int recursionCount;
    int backtrackCount;
    
public:
    SudokuSolver() : board(BOARD_SIZE, std::vector<int>(BOARD_SIZE, 0)),
                     rowMasks(BOARD_SIZE, 0),
                     colMasks(BOARD_SIZE, 0),
                     squareMasks(BOARD_SIZE, 0),
                     recursionCount(0),
                     backtrackCount(0) {}
    
    // Get the 3x3 square number for a given position
    int getSquareNumber(int row, int col) const {
        return (row / SQUARE_SIZE) * SQUARE_SIZE + (col / SQUARE_SIZE);
    }
    
    // Check if a cell is blank (contains 0)
    bool isBlank(int row, int col) const {
        return board[row][col] == 0;
    }
    
    // Check if a value is valid for a given position using bit operations
    bool isValid(int row, int col, int value) const {
        uint16_t mask = MASKS[value];
        int square = getSquareNumber(row, col);
        
        // If any of the masks have this bit set, the value is invalid
        return !(rowMasks[row] & mask) && 
               !(colMasks[col] & mask) && 
               !(squareMasks[square] & mask);
    }
    
    // Set a value in the board and update all masks
    void setCell(int row, int col, int value) {
        if (value == 0) {
            clearCell(row, col);
            return;
        }
        
        board[row][col] = value;
        uint16_t mask = MASKS[value];
        int square = getSquareNumber(row, col);
        
        // Set the bit in all relevant masks
        rowMasks[row] |= mask;
        colMasks[col] |= mask;
        squareMasks[square] |= mask;
    }
    
    // Clear a cell and update all masks
    void clearCell(int row, int col) {
        int value = board[row][col];
        if (value == 0) return;
        
        board[row][col] = 0;
        uint16_t mask = MASKS[value];
        int square = getSquareNumber(row, col);
        
        // Clear the bit in all relevant masks
        rowMasks[row] &= ~mask;
        colMasks[col] &= ~mask;
        squareMasks[square] &= ~mask;
    }
    
    // Find the blank cell with the fewest possible valid values
    std::pair<int, int> findNextBlank() const {
        int minOptions = 10;
        std::pair<int, int> bestCell = {-1, -1};
        
        for (int i = 0; i < BOARD_SIZE; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                if (!isBlank(i, j)) continue;
                
                // Count valid options using bit operations
                int options = countValidOptions(i, j);
                
                if (options < minOptions) {
                    minOptions = options;
                    bestCell = {i, j};
                    if (minOptions == 1) return bestCell; // Early termination
                }
            }
        }
        
        return bestCell;
    }
    
    // Count valid options for a cell using bit operations
    int countValidOptions(int row, int col) const {
        int square = getSquareNumber(row, col);
        uint16_t usedMask = rowMasks[row] | colMasks[col] | squareMasks[square];
        
        // Count unset bits (valid options)
        int count = 0;
        for (int val = 1; val <= 9; val++) {
            if (!(usedMask & MASKS[val])) {
                count++;
            }
        }
        return count;
    }
    
    // Main solving function using backtracking with bit masking
    bool solvePuzzle() {
        recursionCount++;
        
        auto [row, col] = findNextBlank();
        if (row == -1) return true; // No blank cells left
        
        // Try each value from 1 to 9
        for (int val = 1; val <= 9; val++) {
            if (isValid(row, col, val)) {
                setCell(row, col, val);
                
                if (solvePuzzle()) {
                    return true;
                }
                
                clearCell(row, col);
                backtrackCount++;
            }
        }
        
        return false;
    }
    
    // Load a puzzle into the solver
    void loadPuzzle(const std::vector<std::vector<int>>& puzzle) {
        // Clear everything first
        for (int i = 0; i < BOARD_SIZE; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                board[i][j] = 0;
            }
            rowMasks[i] = 0;
            colMasks[i] = 0;
            squareMasks[i] = 0;
        }
        
        // Load the puzzle
        for (int i = 0; i < BOARD_SIZE; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                if (puzzle[i][j] != 0) {
                    setCell(i, j, puzzle[i][j]);
                }
            }
        }
        
        recursionCount = 0;
        backtrackCount = 0;
    }
    
    // Print the board
    void printBoard() const {
        for (int i = 0; i < BOARD_SIZE; i++) {
            if (i % 3 == 0 && i != 0) {
                std::cout << "------+-------+------\n";
            }
            for (int j = 0; j < BOARD_SIZE; j++) {
                if (j % 3 == 0 && j != 0) {
                    std::cout << "| ";
                }
                if (board[i][j] == 0) {
                    std::cout << ". ";
                } else {
                    std::cout << board[i][j] << " ";
                }
            }
            std::cout << "\n";
        }
    }
    
    // Get statistics
    int getRecursionCount() const { return recursionCount; }
    int getBacktrackCount() const { return backtrackCount; }
    
    // Check if the puzzle is solved
    bool isSolved() const {
        for (int i = 0; i < BOARD_SIZE; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                if (board[i][j] == 0) return false;
            }
        }
        return true;
    }
};

// Example usage and demonstration
int main() {
    SudokuSolver solver;
    
    // Example puzzle (same as the "Hard" puzzle from the JavaScript version)
    std::vector<std::vector<int>> puzzle = {
        {0,0,0,6,0,0,4,0,0},
        {7,0,0,0,0,3,6,0,0},
        {0,0,0,0,9,1,0,8,0},
        {0,0,0,0,0,0,0,0,0},
        {0,5,0,1,8,0,0,0,3},
        {0,0,0,3,0,6,0,4,5},
        {0,4,0,2,0,0,0,6,0},
        {9,0,3,0,0,0,0,0,0},
        {0,2,0,0,0,0,1,0,0}
    };
    
    std::cout << "Original Puzzle:\n";
    solver.loadPuzzle(puzzle);
    solver.printBoard();
    
    std::cout << "\nSolving...\n";
    auto start = std::chrono::high_resolution_clock::now();
    
    bool success = solver.solvePuzzle();
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    if (success) {
        std::cout << "\nSolved Puzzle:\n";
        solver.printBoard();
        std::cout << "\nStatistics:\n";
        std::cout << "Recursions: " << solver.getRecursionCount() << "\n";
        std::cout << "Backtracks: " << solver.getBacktrackCount() << "\n";
        std::cout << "Time: " << duration.count() << " microseconds\n";
    } else {
        std::cout << "No solution found!\n";
    }
    
    return 0;
} 