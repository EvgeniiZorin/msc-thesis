import os

def print_comparison_header(comparables: int):
	print(f"********************************************************", file=output)
	print(f"***   Comparison for {comparables}   *********************", file=output)
	print(f"********************************************************", file=output)

def read_file(filename: str) -> list:
	"""
	read and upload to list EXPECTED file
	filename: which file to read 
	listname: name of the list to which lines from 'filename' will be exported
	""" 
	with open(filename, 'r') as f:
		f.readline()
		listname = []
		for line in f:
			listname.append(line.split("\n")[0])
		return listname

def compare_lists(list1: list, list2: list):
	"""
	list1: e.g. mutslist_expected
	list2: e.g. mutslist_test
	"""
	match = []
	onlyInExpected = []
	onlyInTest = []

	# Checking for lines present both in list1 (expected) and list2 (test)
	for item in list1:
		if item in list2 and item not in match:
			match.append(item)
	# Checking for lines present in list1 (expected) only
	for item in list1:
		if item not in list2:
			onlyInExpected.append(item)
	# Checking for lines present in list2 (test) only
	for item in list2:
		if item not in list1:
			onlyInTest.append(item)
	return match, onlyInExpected, onlyInTest

def print_lists_comparisons(mutslist_expected, mutslist_test, match: list, onlyInExpected: list, onlyInTest: list, dimension: int):\
	
	"""
	If the argument 'dimension' is not applicable, please use '-1' for its value
	"""
	print(f"\nItems in both files: ", file=output)
	for iter, item in enumerate(match, 1):
		print(f"{iter}\t{item}", file=output)

	print(f"\nItems in expected only: ", file=output)
	for iter, item in enumerate(onlyInExpected, 1):
		print(f"{iter}\t{item}", file=output)

	print(f"\nItems in test only: ", file=output)
	for iter, item in enumerate(onlyInTest, 1):
		print(f"{iter}\t{item}", file=output)
	if dimension != -1:
		if len(mutslist_expected) == len(mutslist_test) and len(onlyInExpected) == 0 and len(onlyInTest) == 0:
			print(f"\nResult comparison dim {dimension}: OK", file=output)
			print(f"Dim {dimension}: ✅")
		
		if len(mutslist_expected) != len(mutslist_test) or len(onlyInExpected) != 0 or len(onlyInTest) != 0:
			print(f"\nResult comparison dim {dimension}: BAD :(", file=output)
			print(f"Dim {dimension}: ❌")


def conditional_run(expected_file_path, test_file_path, dimension):
	try:
		mutslist_expected = read_file(expected_file_path)
	except FileNotFoundError:
		print(f"Dimension {dimension} expected file not found")
	
	try:
		mutslist_test = read_file(test_file_path)
	except FileNotFoundError:
		print(f"Dimension {dimension} output file not found! ❌" )
	else:
		print(f"\nItems in expected:  {len(mutslist_expected)}  |  Items in test:  {len(mutslist_test)} ", file=output)
		match, onlyInExpected, onlyInTest = compare_lists(mutslist_expected, mutslist_test)
		print_lists_comparisons(mutslist_expected, mutslist_test, match, onlyInExpected, onlyInTest, dimension)

if __name__ == "__main__":
	##########################################################################################
	#####   Variables   ######################################################################
	##########################################################################################
	folder_with_expected = 'test_expected_hypercuboids'
	folder_to_test = 'test_complete_03'
	##########################################################################################
	
	if not os.path.exists(f'{folder_to_test}'):
		print('Please run the command below and then perform this test:\n')
		print(f'python3 VZEM_hypercuboids.py -i test_complete_03.txt -o {folder_to_test}   \n')
	if os.path.exists(f'{folder_to_test}'):
		# dim1_exp = 'test_expected_hypercuboids/VZEM_dim1.txt'; dim1_test = '211127_test_nohypercubes/VZEM_dim1.txt'
		dim1_exp = f'{folder_with_expected}/VZEM_dim1.txt'; dim1_test = f'{folder_to_test}/VZEM_dim1.txt'
		dim2_exp = f'{folder_with_expected}/VZEM_dim2.txt'; dim2_test = f'{folder_to_test}/VZEM_dim2.txt'
		dim3_exp = f'{folder_with_expected}/VZEM_dim3.txt'; dim3_test = f'{folder_to_test}/VZEM_dim3.txt'
		with open('Compare_lines_output.txt', 'w') as output:
			print_comparison_header("Dimension 1")
			conditional_run(
				dim1_exp, 
				dim1_test,
				1
			)
			print_comparison_header("Dimension 2")
			conditional_run(
				dim2_exp, 
				dim2_test, 
				2
			)
			print_comparison_header("Dimension 3")
			conditional_run(
				dim3_exp, 
				dim3_test,
				3
			)

