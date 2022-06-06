# CuboidME

Program for calculating hypercuboids from genotypes and the accompanying programs:
- `CuboidME.py` - the main program for calculating hypercuboids and hyperrectangles; 
- `Format_convert_hypercuboids.ipynb` - python notebook containing scripts to convert fitness landscape datasets into a format usable by CuboidME.py; 
- `Func_test.py` - **main** script for functional test of CuboidME.py; 
- `Func_test_detailed.py` - (beta) secondary test script to test CuboidME.py; 
- `Count_hypercuboids.sh` - a shell scripts to calculate hypercuboids in the hypercuboid output folder of specified path. 

---

# CuboidME.py

**Input options for CuboidME**: 
- .txt file with genotypes
- .txt file with hypercuboids (dim = N)

## Arguments:
- Compulsory:
  - ```-i, --input``` (option 1) input = .txt file with genotypes, if you want to find all hypercuboids
  - ```-f, --first``` (option 2) input = .txt file with genotypes, if you want to find hypercuboids of dim = 1 only
  - ```-j, --jinput``` (option 3) input = .txt file with hypercuboids (dim = N), if you want to find hypercuboids of dim = N+1 only 
- Optional:
  - ```-o, --output``` specify output directory; current dir by default, if no value specified for this argument
  - ```-hc, --hypercubes``` specify 'Yes' if you want to compute hypercuboids (hypercubes + hyperrectangles), or 'No' if you want to only compute hyperrectangles. Default = 'Yes'

## How to use:
*Note: use ```py -3``` or ```python3``` to run, both should work.*
Input - file with genotypes, find all *hypercuboids*:
```py
py -3 CuboidME.py -i test_complete_03.txt -o outputDir
```
Input - file with genotypes, find all *hyperrectangles*:
```py
py -3 CuboidME.py -i test_complete_03.txt -hc No -o outputDir
```
Input - file with genotypes, find hypercuboids of dim = 1 ONLY:
```py
py -3 CuboidME.py -f test_complete_03.txt -o outputDir
```
Input - file with hypercuboids (dim = N), find hypercuboids of dim = N+1 ONLY. E.g. if we have a file with hypercubes of dimension = 2:
```py
py -3 CuboidME.py -j outputDir/VZEM_dim2.txt -o outputDir
```

## Notes:
- *Hypercuboids = hypercubes [H=1] + hyperrectangles [H >= 1]*    
- *H = hamming distance*
- ```test_complete_03.txt``` (standard input; contains exactly 1 combinatorially complete hypercube of dim = 3)
- ```test_complete_03_custom.txt``` (modified version with 1+ mutations at each locus)
- ```test_complete_irregular.txt``` (version for functional test of the program)

---

# Funct_test.py

**Main test script**. Functional test that uses outputs of the algorithm with different parameters (e.g. only first dimension, only N dimension, only hyperrectangles) and compares them with the standard output. Only says if each combination of parameter works; if it says that something doesn't work, you can run ```Funct_test_detailed.py``` to get a more detailed report (*Note: `Func_test_detailed.py` is in beta*). 

## How to use: 
- In cmd line, please run: 
```py
python3 CuboidME.py -i test_complete_03.txt -o test_compare_03_0; python3 CuboidME.py -i test_complete_03.txt -o test_compare_03_1 -hc No; python3 CuboidME.py -f test_complete_03.txt -o test_compare_03_2; python3 CuboidME.py -j test_compare_03_2/VZEM_dim1.txt -o test_compare_03_3; python3 CuboidME.py -i test_files/test_complete_irregular.txt -o test_compare_irregular
``` 
This runs the algorithm with different parameters and puts the output files into specified folders. 
- Open the script and run it. The terminal output should say which parameters worked by printing a green tick mark, or didn't work by printing a red cross. 

# Funct_test_detailed.py
* A more detailed version of ```Funct_test.py```, useful when troubleshooting the algorithm*. 

This is a functional test that compares hypercuboids produced from test_complete_03.txt test file with the expected files. Additionally, it produces a file ```Compare_lines_output.txt``` which details lines matching and not matching between the compared files; this is useful when making major changes to the script. 
- It compares line-by-line output by your program (in this case, ```CuboidME.py```) and the standard output (located in the folder ```test_expected_hypercuboids```)
- It prints output ```Compare_lines_output.txt```, where it lists, for each dimension, matching and non-matching lines in each of the compared files. 

## How to use:
- In cmd line, please run: ```python3 CuboidME.py -i test_complete_03.txt -o test_complete_03
- Then, open ```Compare_lines_VZEM.py``` script, run it, and check cmd line output - if everything is ok, then all arrows are green. 

## Authors

[Evgenii Zorin](https://github.com/EvgeniiZorin) - code
