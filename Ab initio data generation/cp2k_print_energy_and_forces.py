#! /usr/bin/env python

import os
import csv


y = 'E ='
energy = ''
j = 1
l = 3
cell_size = 14
    
for i in range(1001, 5001, 4):
    f = open(str(i) + "_traj_position.xyz", "r")
    all_lines = f.readlines()
    line = all_lines[j]
    if y in line:
        energy = line[line.find(y) + len(y):]


    with open("input.data", 'a') as text_file:
        text_file.write(" begin\n")
        text_file.write("comment revPBE-D3 DZVP-MOLOPT-SR-GTH\n")
        text_file.write('lattice      ' + str(float(cell_size/0.5291)) +  '      0.00      ' + '0.00' + '\n')
        text_file.write('lattice      ' + '0.00      ' +  str(float(cell_size/0.5291)) + '      0.00' + '\n')
        text_file.write('lattice      ' + '0.00      ' +  '0.00      ' + str(float(cell_size/0.5291)) + '\n')
        for b in range(1, 81):
            b += j
            g = open(str(i) + "_traj_position.xyz", "r")
            lines = list(csv.reader(g, delimiter=' ', skipinitialspace=True))
            coord_x = float(lines[b][1]) / 0.5291
            coord_y = float(lines[b][2]) / 0.5291
            coord_z = float(lines[b][3]) / 0.5291
            coord = str(coord_x) + ' ' + str(coord_y) + '  ' + str(coord_z) + '   ' + lines[b][0] 
            b -= j
            b += l
            k = open(str(i) + "_traj_force.xyz", "r")
            lines = list(csv.reader(k, delimiter=' ', skipinitialspace=True))
            forces_x = float(lines[b][3])
            forces_y = float(lines[b][4])
            forces_z = float(lines[b][5])
            forces = str(forces_x) + ' ' + str(forces_y) + '  ' + str(forces_z)          
            text_file.write('atom' + '  ' + coord + '  ' + '0.00' + '  ' +  '0.00' + '  ' + forces + '\n')
        text_file.write('energy' + str(energy))
        text_file.write('charge' + '  ' + '0.00' + '\n')
        text_file.write(' end' + '\n')






