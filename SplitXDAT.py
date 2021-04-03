#!/usr/bin/env python
import numpy as np

def read_xdatcar(lines):
# ---------------------------------------------------------------------------
# Read in the trajectory each configuration is appended as an array to the
# array configurations. Data at the top of the file is stored.
# ---------------------------------------------------------------------------
    """Reading in VASP trajectory. Takes the file as lines.
       Returns:
              title : string
	      scale_factor : float
	      number_ions : list of numbers of each type
	      species : the types of ions
	      positions : a list of lists of all positions"""
    line_count = 0
    total_ions = 0
    lattice = []
    configurations = []
    for line in lines:
        inp = line.split()
        line_count += 1
        if line_count == 1:
	    title = inp[0]
        if line_count == 2:
	    scale_factor = inp[0]
        if line_count >= 3 and line_count <= 5:
	    lattice.append(inp)
        if line_count == 6:
	    species = inp
        if line_count == 7:
	    number_ions = inp
  	    for ion_type in number_ions:
	        total_ions += int(ion_type)
        if len(inp) == 3 and inp[0] == "Direct":
	    positions = []
	    configurations.append(positions)
        if len(inp) == 3 and line_count > 8 and inp[0] != "Direct":
	    positions.append(inp)
    return title, scale_factor, lattice, number_ions, species, configurations
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------


def print_poscars_every_n(title, scale_factor, lattice, number_ions, species, configurations, n):
# ---------------------------------------------------------------------------
# Print out a POSCAR every n steps; set by the print_every parameter
# ---------------------------------------------------------------------------
    counter = 0
    print_every = n
    for configuration in configurations:
        counter += 1
        atom_count = 0
        ion_count = 0
        if counter % print_every == 0:
   	    outfile = open('POSCAR-%s'%counter,'w')
	    outfile.write('%s\n'%(title))
	    outfile.write('%3.2f\n'%(float(scale_factor)))
	    for axis in lattice:
	        for index in range(3):
		    outfile.write('%12.7f'%(float(axis[index])))
		    if index == 2:
		        outfile.write('\n')
	    for atom in species:
		    atom_count += 1
		    outfile.write('%s'% atom)
		    outfile.write('  ')
        	    if atom_count == len(species):
		        outfile.write('\n')
	    for ion in number_ions:
                    ion_count += 1
                    outfile.write('%i'% int(ion))
		    outfile.write('  ')
                    if ion_count == len(number_ions):
                        outfile.write('\n')	
	    for coordinate in configuration:
	        for index in range(3):
		    outfile.write('%12.7f'%(float(coordinate[index])))
		    if index == (len(coordinate)-1):
		        outfile.write('\n')
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
f = open('XDATCAR','r')
lines = f.readlines()
f.close
n = 10
title, scale_factor, lattice, number_ions, species, configurations = read_xdatcar(lines)
print_poscars_every_n(title, scale_factor, lattice, number_ions, species, configurations, n)
