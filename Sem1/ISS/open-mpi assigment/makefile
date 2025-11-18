# Variables
CXX = g++
CXXFLAGS = -O2 -std=c++11 -pthread -fopenmp  # Added -fopenmp here
TARGET = openmp

# List of sizes and number of threads
sizes = 10000 20000 30000 100000 1000000 10000000 50000000
num_threads_list = 2 4 8 16 32 64
num_runs = 5

# Target to build the program
all: $(TARGET)

$(TARGET): openmp.cpp
	$(CXX) $(CXXFLAGS) -o $(TARGET) openmp.cpp

# Run the program with each combination of size and num_threads
run: $(TARGET)
	for run in $(shell seq 1 $(num_runs)); do \
		for size in $(sizes); do \
			for num_threads in $(num_threads_list); do \
				echo "Running with size=$$size and num_threads=$$num_threads"; \
				./$(TARGET) $$size $$num_threads; \
			done \
		done \
	done
