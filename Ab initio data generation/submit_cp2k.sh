#!/bin/bash
#SBATCH --job-name=XXXXX
##SBATCH --account=XXXXX
#SBATCH --time=96:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --mem-per-cpu=3GB

module load module load cp2k/9.1.0 python/3.9.0 mpi/openmpi_4.0.5_gcc_10.2_slurm20 gcc/8.3 cuda/11.1.1
source $CP2KSETUP

srun --mpi=pmix cp2k.popt -i traj_1.inp -o traj_1.out