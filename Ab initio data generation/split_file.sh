#!/bin/bash
#SBATCH --job-name=XXXXX
#SBATCH --account=XXXXX
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=1GB

split -l 82 -d -a 8 FLiNaK-pos-1.xyz
for f in x[0-9]*; do mv "$f" "$((10#${f#x}+1))_traj_position.xyz";  done

split -l 85 -d -a 8 forces.data
for f in x[0-9]*; do mv "$f" "$((10#${f#x}+1))_traj_force.xyz";  done

python3 cp2k_print_energy_and_forces.py
rm {1..5001}_traj_position.xyz
rm {1..5001}_traj_force.xyz

cp input.data ../data_set/input_1.data