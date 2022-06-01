# Epistatic_coefficients_calculator.py   
Script for calculating 2D epistatic coefficients (based on a triangular/thermodynamic matrix) for hypercuboids. 

### Input
There are two required input files. These should be in the directory "Epistatic_coefficients_2D", subdirectory in the format of Epicoeff_databasename_samplesize_nonrand_date, e.g. Epicoeff_IPDS1_300_nonrand_220115. 
1. Database file with genotypes and fitness values; for reference, see ```test_functional/test_complete_03.txt```; 
2. (Options) File with hypercubes of dimension 2 (e.g. ```test_functional/hypercubes_2.txt```) AND/OR file with hyperrectangles of dimension 2 (e.g. ```test_functional/VZEM_dim2.txt```). 

### How to run
- In ```if __name__ == '__main__':```, change variables to indicate your desired input: name of database, sample size, and date. Note that database name should be standardised to look like Databasename_proc2_samplesize.txt, e.g. IPDS1_proc2_300.txt; 
- Comment out hypercubes or hyperrectangles options, if you don't need them; 
- Run the script

# Functional test
test_functional.py   

### How to run
- From script: simply run it :) it will automatically run the Epistatic_coefficients_calculator.py script in its current state with standard databases, then check if output (epicoeffs) matches the expected output. 
- From the terminal: ```python -m unittest Unit_Test```
