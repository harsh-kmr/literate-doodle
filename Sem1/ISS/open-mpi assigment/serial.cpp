#include <iostream>
#include <fstream>  
#include <cstdlib>
#include <chrono>  
#include <climits>

void generateRandomArray(int* arr, int size, int minValue = 0, int maxValue = 100) {
    std::srand(std::time(nullptr));

    for (int i = 0; i < size; ++i) {
        arr[i] = minValue + std::rand() % (maxValue - minValue + 1);
    }
}

void sumArray(int* A, int* B, int size) {
    B[0] = A[0];
    for (int i = 1; i < size; i++) {
        B[i] = B[i-1] + A[i];
    }
}

int verifyArray(int* C, int* B, int size) {
    for (int i = 0; i < size; i++) {
        if (C[i] != B[i]) {
            return 0;
        }
    }
    return 1;
}