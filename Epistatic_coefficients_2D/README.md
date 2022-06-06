# Epistatic_coefficients_calculator.py   
Script for calculating 2D epistatic coefficients (based on a triangular/thermodynamic matrix) for hypercuboids. 

### Input
There are three required input files:
1. 2D hypercubes for a dataset sample: `hypercubes_2.txt` **OR** 2D hyperrectangles for a dataset sample: `VZEM_dim2.txt`
3. Dataset sample of a large fitness landscape: `<database name>_proc2_<sample size>.txt` (*for reference, see `test_functional/test_complete_03.txt`*);
The abovementioned files should be in the same directory named as follows: 
`Epicoeff_<database name>_<sample size>_nonrand_<date>`, for example, `Epicoeff_IPDS1_1000_nonrand_220115`.


### How to run
- In ```if __name__ == '__main__':```, change variables to indicate your desired input: name of database, sample size, and date. Note that database name should be standardised to look like Databasename_proc2_samplesize.txt, e.g. IPDS1_proc2_300.txt; 
```py
database_name = 'IPDS1'
sample_size = 1000
date = '220202'
```
- Comment out hypercubes or hyperrectangles options, if you don't need them; 
- Run the script

# Functional test
test_functional.py   

### How to run
- From script: simply run it :) it will automatically run the Epistatic_coefficients_calculator.py script in its current state with standard databases, then check if output (epicoeffs) matches the expected output. 
- From the terminal: ```python -m unittest Unit_Test```
