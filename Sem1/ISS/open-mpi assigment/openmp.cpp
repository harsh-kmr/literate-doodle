#include <omp.h>
#include <iostream>
#include <fstream>
#include <cstdlib>
#include <chrono>
#include <climits>
#include <vector>
#include "serial.cpp"

void parallel_sumArray(int* A, int* B, int size, int num_threads, int block_size, int blocks_per_thread, std::vector<int>& partial_sums, std::vector<int>& block_starts, std::vector<int>& block_ends, int num_blocks) {

    #pragma omp parallel num_threads(num_threads)
    {
        int tid = omp_get_thread_num();
        int start = tid * blocks_per_thread * block_size;
        int end = std::min((tid + 1) * blocks_per_thread * block_size, size);
        block_starts[tid] = start;
        block_ends[tid] = end;
        if (start < size) {  
            B[start] = A[start];
            for (int i = start + 1; i < end; i++) {
                B[i] = B[i - 1] + A[i];
            }
            partial_sums[tid] = B[end - 1];
            
        }
    }

    for (int i = 1; i < num_threads; i++) {
        partial_sums[i] += partial_sums[i - 1];
    }


    #pragma omp parallel num_threads(num_threads)
    {
        int tid = omp_get_thread_num();
        int offset = (tid == 0) ? 0 : partial_sums[tid - 1];
        int start = block_starts[tid];
        int end = block_ends[tid];
        if (start < size) {
            for (int i = start; i < end; i++) {
                B[i] += offset;
            }
        }
    }
}


int main(int argc, char* argv[]) {

    if (argc < 3) {
        std::cerr << "Usage: " << argv[0] << " <size> <num_threads>" << std::endl;
        return 1;
    }

    int size = std::atoi(argv[1]);
    int num_threads = std::atoi(argv[2]);

    int* A = new int[size];
    int* B = new int[size];
    int* C = new int[size];

    generateRandomArray(A, size, 0, 10);

    std::ofstream logFile("logfile.txt", std::ios::app);
    if (!logFile) {
        std::cerr << "Error opening file for writing." << std::endl;
        delete[] A;
        delete[] B;
        delete[] C;
        return 1;
    }

    int block_size = 1024;
    std::vector<int> partial_sums(num_threads, 0);  
    std::vector<int> block_starts(num_threads, 0);  
    std::vector<int> block_ends(num_threads, 0);    
    int num_blocks = (size + block_size - 1) / block_size;
    int blocks_per_thread = (num_blocks + num_threads - 1) / num_threads;

    auto start = std::chrono::high_resolution_clock::now();
    parallel_sumArray(A, B, size, num_threads, block_size, blocks_per_thread, partial_sums, block_starts, block_ends, num_blocks);
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);
    logFile << "Time taken by parallel_sumArray: " << duration.count() << " nanoseconds." << " for size: " << size << " and thread num :" << num_threads << std::endl;

    auto start_serial = std::chrono::high_resolution_clock::now();
    sumArray(A, C, size);
    auto end_serial = std::chrono::high_resolution_clock::now();
    auto duration_serial = std::chrono::duration_cast<std::chrono::nanoseconds>(end_serial - start_serial);
    logFile << "Time taken by sumArray: " << duration_serial.count() << " nanoseconds." << " for size: " << size << std::endl;

    logFile << "Speedup: " << (double)duration_serial.count() / duration.count() << std::endl;

    if (verifyArray(C, B, size)) {
        logFile << "Arrays are equal." << std::endl;
    } else {
        logFile << "Arrays are not equal." << std::endl;
    }

    logFile << std::endl;
    logFile << std::endl;

    logFile.close();
    delete[] A;
    delete[] B;
    delete[] C;

    return 0;
}