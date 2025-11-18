#!/bin/bash
#SBATCH --job-name=mpi_search    
#SBATCH --nodes=4                    
#SBATCH --tasks-per-node=32          
#SBATCH --nodelist=node[4-7]     

module load openmpi
cd $SLURM_SUBMIT_DIR

mpicxx -o mpi_dummy mpi_dummy.cpp

process_counts=(1 2 4 8 16 32 64)

for p in "${process_counts[@]}"; do
    echo "Running with $p processes"
    mpirun --map-by core -np $p ./mpi_dummy > /dev/null
 
    for i in {1..20}; do
        mpirun --map-by core -np $p ./mpi_dummy >> results_${p}_procs.txt
    done
    echo "----------------------------------------" >> results_${p}_procs.txt
done


make

make run