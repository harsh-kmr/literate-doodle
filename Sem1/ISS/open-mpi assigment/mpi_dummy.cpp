#include <mpi.h>
#include <iostream>
#include <cstdlib>
#include <ctime>
#include <chrono>

// Generate a random array of integers
void generateRandomArray(int* arr, int size, int minValue = 1, int maxValue = 5000000) {
    srand(time(nullptr));
    for (int i = 0; i < size; ++i) {
        arr[i] = minValue + rand() % maxValue;
    }
}

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    
    const int size = 10000000;  
    int* A = nullptr;
    int TARGET;
    int rank, world_size;
    
    MPI_Comm_rank(MPI_COMM_WORLD, &rank); // Get the rank of the process
    MPI_Comm_size(MPI_COMM_WORLD, &world_size); // Get the number of processes

    const int local_size = size / world_size;
    int* local_array = new int[local_size];

    if (rank == 0) {
        A = new int[size];
        generateRandomArray(A, size);
        TARGET = A[rand() % size]; 
        
    }

    MPI_Bcast(&TARGET, 1, MPI_INT, 0, MPI_COMM_WORLD); // Broadcast the target value

    MPI_Scatter(A, local_size, MPI_INT, 
                local_array, local_size, MPI_INT, 
                0, MPI_COMM_WORLD); // Scatter the array

    MPI_Barrier(MPI_COMM_WORLD);


    int found_index = -1;
    int global_found = 0;
    MPI_Request request;
    MPI_Status status;

    if (world_size > 1) {
        MPI_Irecv(&global_found, 1, MPI_INT, MPI_ANY_SOURCE, 0, MPI_COMM_WORLD, &request); // Non-blocking receive
    }

    auto start_time = std::chrono::high_resolution_clock::now(); // Start time

    int k = 0;
    for (int i = 0; i < local_size && !global_found; ++i) {
        k += 1;
        if (local_array[i] == TARGET) {
            found_index = rank * local_size + i;  
            global_found = 1;
            
            if (world_size > 1) {
                for (int j = 0; j < world_size; ++j) {
                    if (j != rank) {
                        MPI_Send(&global_found, 1, MPI_INT, j, 0, MPI_COMM_WORLD); // Send the found flag
                    }
                }
            }
            break;
        }

        if (world_size > 1 && k % 1000 == 0) {
            int flag = 0;
            MPI_Test(&request, &flag, &status);  // Test if the global found flag is set
            if (flag) {
                global_found = 1;
                break;
            }
        }
    }

    if (world_size > 1 && !global_found) {
        MPI_Wait(&request, &status);
    }


    int global_index;
    MPI_Allreduce(&found_index, &global_index, 1, MPI_INT, MPI_MAX, MPI_COMM_WORLD); // Find the global index

    auto end_time = std::chrono::high_resolution_clock::now(); // End time
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(
        end_time - start_time).count();     // Calculate the duration

    if (rank == 0) {
        if (global_index != -1) {
            std::cout << "Target " << TARGET << " found at index " << global_index << std::endl;
            std::cout << "Search time: " << duration << " microseconds" << std::endl;
        } else {
            std::cout << "Target not found" << std::endl;
        }
    }

    delete[] local_array;
    if (rank == 0) {
        delete[] A;
    }

    MPI_Finalize();
    return 0;
}