
import csv, argparse, sys, os, datetime, time
import colorama; from colorama import Style, Fore, Back; colorama.init(autoreset=True)

def check_input(line: str, rownumber: int):
    """
    Checks input rows for valid format, i.e. that the first column consists of amino acids in the correct notation. \n
    Used ONLY when creating dimension 1 from the file with genotypes. 
    """
    amino_acids_list = ['G', 'A', 'V', 'L', 'I', 'M', 'F', 'W', 'P', 'S', 'T', 'C', 'Y', 'N', 'Q', 'D', 'E', 'K', 'R', 'H', 'Z', '*']
    frames = line.split(':')
    # Check each colon-separated mutation from column one
    for a in frames:
        if a[:-1].isdigit() & (str(a[-1]).upper() in amino_acids_list):
            continue
        else:
            raise NameError(f'Error: invalid input format in the genotype file at line {rownumber + 2}')


def read_genotypes(filename: str) -> list:
    """
    Read the genotypes from the 'filename' file with genotypes. Skips the header. \n
    Used ONLY when creating dimension 1 from file with genotypes.
    """
    genotypes = list()
    with open(filename, 'r') as filehandle:
        # Skip header line
        filehandle.readline()
        for index, line in enumerate(filehandle):
            first = line.split('\t')[0]
            first = first.replace('\n', '')
            if first == '' or first == 'wt':
                genotypes.append(('0Z',))
            else:
                check_input(first, index)
                genotypes.append(tuple(first.split(':')))
    return genotypes

def read_diagonals_dimN(filename:str) -> list:
    """
    Parses hypercube file (dim = N) and collects DIAGONALS. \n
    Used in creating hypercubes of dim > 1.
    """
    diagonals = list()
    with open(filename, 'r') as filehandle:
        filehandle.readline()
        for index, line in enumerate(filehandle):
            first = line.split('\t')[0]
            diagonals.append(first)
    return diagonals

def read_genotypes_dimN(filename: str) -> list:
    """
    Parses hypercube file (dim = N) and collects GENOTYPES. \n
    Used in creating hypercubes of dim > 1.
    """
    genotypes = list()
    with open(filename, 'r') as filehandle:
        filehandle.readline()
        for line in filehandle:
            first = line.split('\n')[0]
            first = first.split('\t')[1:]
            genotypes.append(tuple(first))
    return genotypes

def get_delta(genotype1: str, genotype2: str) -> str:
    """
    Return difference between 'genotype1' and 'genotype2' as
    alphabetically ordered list of mutations.
    """
    # Process genotype1
    empty_list = list()
    for item in genotype1:
        subitem = item.split(':')
        for subsubitem in subitem:
            empty_list.append(subsubitem)
    genotype1 = tuple(empty_list)
    # Process genotype2
    empty_list = list()
    for item in genotype2:
        subitem = item.split(':')
        for subsubitem in subitem:
            empty_list.append(subsubitem)
    genotype2 = tuple(empty_list)

    s1 = set(genotype1)
    s2 = set(genotype2)
    # Make the set empty if a genotype in s1 or s2 is '0Z', i.e. the wild-type variant of an amino acid
    if len(s1) == 1 and '0Z' in s1:
        s1 = set()
    if len(s2) == 1 and '0Z' in s2:
        s2 = set()

    dpos_letters = dict((u[:-1], u[-1]) for u in s1.difference(s2))
    Dpos_letters = dict((u[:-1], u[-1]) for u in s2.difference(s1))
    positions = sorted(int(u) for u in set(list(dpos_letters.keys()) + list(Dpos_letters.keys())))
    reverse = False
    # Processing first position, which defines 'reverse' or 'forward'
    pos = str(positions[0])
    if pos in dpos_letters and pos in Dpos_letters:
        if dpos_letters[pos] < Dpos_letters[pos]:
            change = dpos_letters[pos] + pos + Dpos_letters[pos]
        else:
            change = Dpos_letters[pos] + pos + dpos_letters[pos]
            reverse = True
    elif pos in dpos_letters:
        change = dpos_letters[pos] + pos + 'Z'
    else:
        change = Dpos_letters[pos] + pos + 'Z'
        reverse = True
    delta = [change]
    # Now adding all other mutations
    for pos in positions[1:]:
        pos = str(pos)
        if pos in dpos_letters and pos in Dpos_letters:
            if not (reverse):
                change = dpos_letters[pos] + pos + Dpos_letters[pos]
            else:
                change = Dpos_letters[pos] + pos + dpos_letters[pos]
        elif pos in dpos_letters:
            if not (reverse):
                change = dpos_letters[pos] + pos + 'Z'
            else:
                change = 'Z' + pos + dpos_letters[pos]
        else:
            if reverse:
                change = Dpos_letters[pos] + pos + 'Z'
            else:
                change = 'Z' + pos + Dpos_letters[pos]
        delta.append(change)
    if reverse:
        return 'reverse', tuple(sorted(delta))
    else:
        return 'forward', tuple(sorted(delta))

def write_to_file(dimension, lines):
    """
    Reads variable (list) containing hypercubes of dim = N and writes them to the file output, same dim. 
    """
    # If output folder is specified
    if args.output is not None:
        if not os.path.exists(args.output):
            os.makedirs(args.output)
        with open(f'{args.output}/VZEM_dim{dimension}.txt', 'w') as fh:
            print("Heading", file=fh)
            for line in sorted(lines):
                print(line, file=fh)
    # If output folder is NOT specified
    elif args.output is None:
        with open(f'VZEM_dim{dimension}.txt', 'w') as fh:
            print("Heading", file=fh)
            for line in sorted(lines):
                print(line, file=fh)

def diagonal_maker(diag1, diag2):
    """
    When processing a dimension, makes a diagonal from matching genotypes 
    by combining their diagonals. \n
    Used when combining diagonals for dimensions >= 2.
    """
    templist = []
    if type(diag1) == str:
        templist.append(diag1)
    else:
        templist.append(';'.join(diag1))
    if type(diag2) == str:
        templist.append(diag2)
    else:
        templist.append(';'.join(diag2))

    templist2 = []
    for i in templist:
        templist2 += i.split(':')
    diag2var = ':'.join(sorted(templist2))
    return diag2var

def start_from_custom_dim(filename: str) -> int:
	"""
    If you want to start from a specific file with already-calculated hypercubes (dim = N), \n
    this function will calculate N+1 hypercubes. \n
    INPUT
    ---
        (str) full name of the file, e.g. 'VZEM_dim2.txt'
    
    RETURNS
    ---
        int, e.g. 2
	"""
	filename = filename.split(".")[0][-1]
	return int(filename)

def process_dimension_1(genotypes):
    """
    Master file for reading 

    USED
    ---
        When reading genotypes file, creating dim1 
    """
    dim1_time = time.time()
    print(f"Processing dimension {Fore.YELLOW}{Style.BRIGHT}{dimension}{Style.RESET_ALL}...")
    # write pairs
    lines = list()
    for i in range(0, len(genotypes)-1):
        for j in range(i+1, len(genotypes)):
            direction, delta = get_delta(genotypes[i], genotypes[j])
            if args.hypercubes in ['Yes', 'yes']:
                if direction == 'forward':
                    lines.append(str(';'.join(delta)) + '\t' + ':'.join(genotypes[i]) + '\t' + ':'.join(genotypes[j]))
                if direction == 'reverse':
                    lines.append(str(';'.join(delta)) + '\t' + ':'.join(genotypes[j]) + '\t' + ':'.join(genotypes[i]))
            if args.hypercubes in ['No', 'no']:
                if len(delta) != 1:
                    if direction == 'forward':
                        lines.append(str(';'.join(delta)) + '\t' + ':'.join(genotypes[i]) + '\t' + ':'.join(genotypes[j]))
                    if direction == 'reverse':
                        lines.append(str(';'.join(delta)) + '\t' + ':'.join(genotypes[j]) + '\t' + ':'.join(genotypes[i]))
    print(f"   Found hypercuboids: N = {Fore.GREEN}{Style.BRIGHT}{len(lines)}")
    # print(f"   Runtime (sec): {Fore.GREEN}{round(time.time() - start_time, 5)}{colour.reset}")
    print(f"   Runtime (sec) for dim1: {round(time.time() - dim1_time, 5)}")
    global total_number_of_hypercuboids
    total_number_of_hypercuboids = total_number_of_hypercuboids + len(lines)
    write_to_file(1, lines)

def process_dimension_N(dimension: int):
    """
    Function to process diagonals in creating hypercubes of dimensionality N >= 2

    RETURNS
    ---
        'lines' - a list with mutations
    """
    print(f"Processing dimension {Fore.YELLOW}{Style.BRIGHT}{dimension}{Style.RESET_ALL}...")
    # Creating dim_N hypercubes
    # Read diagonals from dim_N-1 file:
    if args.output is None:
        diagonals = read_diagonals_dimN(f"VZEM_dim{dimension-1}.txt")
    elif args.output is not None and args.jinput is None:
        diagonals = read_diagonals_dimN(f"{args.output}/VZEM_dim{dimension-1}.txt")
    elif args.output is not None and args.jinput is not None:
        diagonals = read_diagonals_dimN(f"{args.jinput}")
    # print(diagonals)
    # print(len(diagonals))

    # Read genotypes from dim_N-1 file:
    if args.output is None:
        genotypes = read_genotypes_dimN(f"VZEM_dim{dimension-1}.txt")
    elif args.output is not None and args.jinput is None:
        genotypes = read_genotypes_dimN(f"{args.output}/VZEM_dim{dimension-1}.txt")
    elif args.output is not None and args.jinput is not None:
        genotypes = read_genotypes_dimN(f"{args.jinput}")
    # print(genotypes)
    # print(len(genotypes))

    lines = list()
    for i in range(0, len(diagonals)-1):
        for j in range(i+1, len(diagonals)):
            if diagonals[i] == diagonals[j]:
                # print(f"{genotypes[i]} + {genotypes[j]} ?")
                # print(get_delta(genotypes[i], genotypes[j]))
                direction, delta = get_delta(genotypes[i][0].split(':'), genotypes[j][0].split(':'))
                # print(direction, delta)
                # if args.hypercubes in ['Yes', 'yes']:
                if direction == 'reverse':
                    newlist = []
                    newlist.append(diagonals[i])
                    for item in delta:
                        newlist.append(item)

                    newlist.sort()
                    # print(f"Old diagonal: {diagonals[i]}")
                    # print(f"New diagonal: {delta}")
                    # print(f"FINAL OUTPUT - Diagonal: {newlist}; From: {genotypes[j][0]}; To: {genotypes[i][1]} ")
                    # saving to 'lines':
                    diagonal = diagonal_maker(diagonals[i], delta)
                    lines.append( str(diagonal) + '\t' + genotypes[j][0] + '\t' + genotypes[i][1] )

                if direction == 'forward':
                    newlist = []
                    newlist.append(diagonals[i])
                    for item in delta:
                        newlist.append(item)
                    newlist.sort()
                    # print(f"Old diagonal: {diagonals[i]}")
                    # print(f"New diagonal: {delta}")
                    # print(f"FINAL OUTPUT - Diagonal: {newlist}; From {genotypes[i][0]}; To: {genotypes[j][1]}")
                    # saving to 'lines':
                    diagonal = diagonal_maker(diagonals[i], delta)
                    lines.append( diagonal + '\t' + genotypes[i][0] + '\t' + genotypes[j][1] )
                
    lines = list(set(lines))
    global total_number_of_hypercuboids
    total_number_of_hypercuboids = total_number_of_hypercuboids + len(lines)
    return lines


if __name__ == '__main__':
    start_time = time.time()
    # Process arguments
    parser = argparse.ArgumentParser(description="Run the program by running the commands in the single quotes: 1) 'py -3 CuboidME.py -i test_complete_03.txt -hc No -o test_complete_03' or 2) 'python3 CuboidME.py -i test_complete_03.txt -hc No -o test_complete_03' ")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--input', help='the filename with the list of measured genotypes; input for processing all dimensions present'
                                                ' e.g. "test_complete_03.txt"')
    group.add_argument('-f', '--first', help='if you want to read list of genotypes and create 1D hypercuboids ONLY'
                                                ' e.g. "test_complete_03.txt"')
    group.add_argument('-j', '--jinput', help='the filename with the list of already-calculated hypercubes (dim N; N >= 1), which you use as input to calculate hypercubes of dimension (N+1),'
                                                ' e.g. "VZEM_dim2.txt"')
    parser.add_argument('-hc', '--hypercubes', help='Do you want to calculate hypercubes along with hyperrectangles? Default is "Yes", where you calculate hypercuboids (hypercubes + hyperrectangles)', default="Yes")
    parser.add_argument('-o', '--output', help='name of non-existing folder to store intermediate and result files.'
                                                ' If nothing specified for this argument, the algorithm outputs all processed hypercuboids into the current directory')
    # parser.add_argument('-v', '--verbose', help='print detailed information', action='store_true')
    args = parser.parse_args()
    print('========================= CuboidME, version 9.1.1 =================================')
    print(f'Program started at (hh:mm:ss): {datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second} \nArguments passed: {args}\n')

    total_number_of_hypercuboids = 0

    ###############################################################################
    #####     Option 1                                                        #####
    #####     INPUT: genotypes                                                #####
    #####     OUTPUT: all possible dimensions of hypercuboids                 #####
    ###############################################################################
    if args.input is not None:
        # Process dimension 1
        dimension = 1
        genotypes = read_genotypes(args.input)
        process_dimension_1(genotypes)
        # Process dimension 2
        dimension = 2
        while True:
            dim_time = time.time()
            lines = process_dimension_N(dimension)
            if len(lines) != 0:
                print(f"   Found hypercuboids: N = {Fore.GREEN}{Style.BRIGHT}{len(lines)}")
                print(f"   Runtime (sec) for dim{dimension} : {round(time.time() - dim_time, 5)}")
                write_to_file(dimension, lines)
                dimension += 1
            if len(lines) == 0:
                print(f"   Nothing found for this dimension.")
                break
        print(f"{Fore.GREEN}{Style.BRIGHT}Successful end!")
    print(f"Total runtime (sec): {Fore.GREEN}{Style.BRIGHT}{round(time.time() - start_time, 5)}")    
    print(f"Total number of hypercuboids: {total_number_of_hypercuboids}")
    ###############################################################################
    #####     Option 2                                                        #####
    #####     INPUT: genotypes                                                #####
    #####     OUTPUT: hypercuboids of dim = 1 ONLY                            #####
    ###############################################################################
    if args.first is not None and args.input is None and args.jinput is None:
        # Process dimension 1
        dimension = 1
        genotypes = read_genotypes(args.first)
        process_dimension_1(genotypes)

    ###############################################################################
    #####     Option 3                                                        #####
    #####     INPUT: hypercuboids, dim = N                                    #####
    #####     OUTPUT: hypercuboids, dim = N+1                                 #####
    ###############################################################################
    if args.jinput is not None:
        # Start with hypercubes
        if start_from_custom_dim(args.jinput) >= 1:
            dimension = start_from_custom_dim(args.jinput) + 1
            print(f"Dimension to read: {dimension - 1}")
            print(f"Dimension to create: {dimension}")
            # while True:
            lines = process_dimension_N(dimension)
            if len(lines) != 0:
                print(f"   Found hypercuboids: N = {Fore.GREEN}{Style.BRIGHT}{len(lines)}")
                write_to_file(dimension, lines)
                dimension += 1
            if len(lines) == 0:
                print(f"   {Fore.RED}{Style.BRIGHT}Nothing found here.")
                
            print(f"{Fore.GREEN}{Style.BRIGHT}Successful end!")
        else:
            print("Something is wrong, check your input...")
