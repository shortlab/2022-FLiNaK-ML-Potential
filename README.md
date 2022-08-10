# 2022-FLiNaK-ML-Potential
Repository for Hervé Caralp’s MD manuscript.

This repository provides a step-by-step guideline on how to build and run a Neural Network Potential (NNP) for a FLiNaK system using ab initio Molecular Dynamics (AIMD). Example input files as well as output files (in some cases) will be provided for each step. This is a three-step process, and each process will have its separate folder containing relevant scripts: 
1.	 Ab initio data generation
2.	Interatomic potential training
3.	Molecular dynamics simulations
In order to proceed, several software packages need to be installed locally or on your cluster. These are: 
•	Python 3.6 (or higher)
•	ASE 3.13.0
•	Packmol
•	CP2K
•	LAMMPS molecular dynamics open-source code
•	Have LAMMPS installed as Python module
•	Have the N2P2 LAMMPS (add link to N2P2 github)
The use of a high-performance supercomputer is recommended. It is also strongly suggested to read the LAMMPS manual in order to understand all the commands used and how to tune the command arguments.

# **1.	Ab initio data generation**


The first step in building an NNP is to generate forces and positions from ab initio molecular dynamics simulation which can then be used as input for the neural network training. First, the initial configurations of the atomic system (in our example, 80) needs to be generated. This can be done on your local computer (recommended) or on a high-performance supercomputer using packmol. Information on how to compile and use packmol can be found here. Note that a folder containing the input files for an 80-atom system is included in the corresponding folder. Once packmol set up, go to the path where the package is installed and enter the following command: 
packmol < opt.inp
 This will generate a .xyz file in the same directory. This file is your initial configuration file and will be required to run MD simulations.
Once the initial configuration generated, CP2K is used to perform AIMD. Here are the main modeling choices made in the provided input file. Note that a total of 120 different simulations were required for generating a robust interatomic potential, where temperature, box size and canonical ensembles were the variables at play.  
-	A box size of 9x9x9 Å
-	A temperature of 1000K at 1 bar
-	An NVT ensemble with the CSVR thermostat (specific to CP2K)
-	A simulation length of 10,000 steps with 0.5 fs timestep
-	The DZVP-MOLOPT-SR-GTH basis set with PBE correlation function. 
All this information can be found in the traj.inp file. When the input file is ready, the job can be submitted to the supercomputer using the submit.sh file. The following command will submit your job: 
sbatch submit.sh
The simulation will then run for several hours (up to 48 hours in the case of this input file, depending on the allocated computational power). Multiple files will be created during the simulation. A good indicator to verify if the simulation is going as planned is to open the .ener file and look at the “used time” column; the first few steps should be long, and then diminish. If after ~ 200 steps (for this input file) the time is repeatedly larger than 100s, then there might a problem with the simulation. In that case, cancel the job, change the initial configuration or the size of the box, and start again. 
Once the simulation done, we can prepare the output data for the next step. Two files come at play: 
-	Split_files.sh
-	Cp2k_print_energy_and_forces.py
These two files will split the position and forces output files and merge relevant parts together. Make sure to have loaded the python and ase module before submitting the split_files.sh file, as failing to do so will refrain the .py file from working. Also, I would recommend to NOT go in the directory as long as the split_files.sh job is running. A large number of temporary files are created and going in the directory might make your computer crash (it happened several times to me). Simply monitor the job list and you will be fine. In the .py file, on row 13, we ask to only collect the forces and positions from every 4 steps after the 1001 step. The reason for every 4 is that we do not need all positions and forces from one simulation. The reason for only looking after 1001 steps is because we assume the first 1000 steps correspond to the equilibrium section of the simulation, giving enough time to CP2K to bring the system to its equilibrated configuration. Once done, two additional files will be available: 
-	Forces.data
-	Input.data
In a separate folder, add all the input.data files and number them in a way that the inputs look like this: input_1.data, input_2.data etc. Note that in the included split_file.sh file, the last command line will automatically create a new folder named “data_set” and add the input.data file to it. Once all input.data files are set in the folder, they need to be merged together. This is done by executing the merging_data.py script. This will generate one large file containing all the input.data files. Rename this how you like and paste it in a new folder, but make sure to keep the file as .data. 

# **2.	Interatomic potential training**
Now that we have a file containing all the necessary AIMD information, we can get started on the neural network training. In your new folder containing the large .data file, add the input.nn file included in the “Interatomic potential training” folder. 
