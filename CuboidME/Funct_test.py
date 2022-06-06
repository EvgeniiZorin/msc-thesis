import os
import sys


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
	if dimension != -1:
		if len(mutslist_expected) == len(mutslist_test) and len(onlyInExpected) == 0 and len(onlyInTest) == 0:
			# Good - do nothing
			global count_of_mismatches
			count_of_mismatches += 0
		if len(mutslist_expected) != len(mutslist_test) or len(onlyInExpected) != 0 or len(onlyInTest) != 0:
			# Bad - add to count of mismatches
			count_of_mismatches += 1
	# print(count_of_mismatches)
			

def conditional_run(expected_file_path, test_file_path, dimension):
	try:
		mutslist_expected = read_file(expected_file_path)
	except FileNotFoundError:
		print(expected_file_path)
		print(f"Dimension {dimension} expected file not found")
	
	try:
		mutslist_test = read_file(test_file_path)
	except FileNotFoundError:
		print(f"Dimension {dimension} output file not found! ❌" )
	else:
		match, onlyInExpected, onlyInTest = compare_lists(mutslist_expected, mutslist_test)
		print_lists_comparisons(mutslist_expected, mutslist_test, match, onlyInExpected, onlyInTest, dimension)

def launch(index, start_dim, end_dim):
	global count_of_mismatches
	count_of_mismatches = 0
	print(f"{commands_to_test[index]}")
	for i in range(start_dim, end_dim+1):
		dimN_exp = f'{folder_expected[index]}/VZEM_dim{i}.txt'; dimN_test = f'{folder_to_test[index]}/VZEM_dim{i}.txt'
		conditional_run(
			dimN_exp, dimN_test, i
		)
	if count_of_mismatches == 0:
		print(f"   ✅")
		return 1
	else:
		print('   ❌')
		return -1


if __name__ == "__main__":
	folder_expected = [
		# test_complete_03 with different commands
		'test_files/test_expected_03_0',   # index 0: input, output
		'test_files/test_expected_03_1',   # index 1: input, output, -hc No
		'test_files/test_expected_03_2',   # index 2: first, output
		'test_files/test_expected_03_3',   # index 3: jinput, output
		# test irregular
		'test_files/test_expected_irregular'    # index 4: input, output
	]
	number_of_files = [
		3, 
		2,
		1, 
		1, 
		1
	]
	folder_to_test = [
		'test_compare_03_0', 
		'test_compare_03_1', 
		'test_compare_03_2', 
		'test_compare_03_3', 
		'test_compare_irregular'
	]
	commands_to_test = [
		f'python3 CuboidME.py -i test_complete_03.txt -o {folder_to_test[0]}', 
		f'python3 CuboidME.py -i test_complete_03.txt -o {folder_to_test[1]} -hc No', 
		f'python3 CuboidME.py -f test_complete_03.txt -o {folder_to_test[2]}', 
		f'python3 CuboidME.py -j {folder_to_test[2]}/VZEM_dim1.txt -o {folder_to_test[3]}', 
		f'python3 CuboidME.py -i test_files/test_complete_irregular.txt -o {folder_to_test[4]}'
	]

	##########################################################################################
	for item in folder_to_test:
		if not os.path.exists(f'{item}'):
			print('------------------------------------------------------------------------------------------------------')
			print(f'{item} folder doesnt exist!')
			print('Please run the command below and then run Funct_test.py again:\n')
			print('; '.join(commands_to_test))
			print('------------------------------------------------------------------------------------------------------')
			# print(f'python3 CuboidME.py -i test_complete_03.txt -o {folder_to_test[0]}; python3 CuboidME.py -i test_complete_03.txt -o {folder_to_test[1]}   \n')
			sys.exit()
	results = []
	# Test index 0 
	# launch(0, 1, 3)
	results.append(launch(0,1,3))
	# Test index 1
	# launch(1, 1, 2)
	results.append(launch(1,1,2))
	# Test index 2
	# launch(2, 1, 1)
	results.append(launch(2,1,1))
	# Test index 3
	# launch(3, 2, 2)
	results.append(launch(3,2,2))
	# Test index 4
	# launch(4, 1, 1)
	results.append(launch(4,1,1))
	print('-'*100)
	print(f'Passed: {results.count(1)}')
	print(f'Failed: {results.count(-1)}')