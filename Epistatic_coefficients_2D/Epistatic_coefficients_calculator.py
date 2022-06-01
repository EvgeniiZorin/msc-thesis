"""
Conditions: 
- The two input files - hyperrectangles and fitland database - ) should have the first row as the heading row - it will be skipped. 
"""
extended_output_flag = True

##### For unittest: 
##### Run 1 - for hyperrectangles from test_complete_03.txt: #######################################
# hypercuboids_input = 'Unit_Test/VZEM_dim2.txt'
# database_fitland_input = 'Unit_Test/test_complete_03.txt'
# output_epistatic_coefficients = 'test_epistatic_coefficients_hyperrectangles.txt'
##### Run 2 - for hypercubes from test_complete_03.txt: ############################################
# hypercuboids_input = 'Unit_Test/hypercubes_2.txt'
# database_fitland_input = 'Unit_Test/test_complete_03.txt'
# output_epistatic_coefficients = 'test_epistatic_coefficients_hypercubeME.txt'
##### Afterwards, run Unit_Test.py script ##########################################################
# hypercuboids_input = '211210_epicoeff_IPDS11_100/hypercubes_2.txt'
# database_fitland_input = '211210_epicoeff_IPDS11_100_IPDS11_100.txt'
# output_epistatic_coefficients = '211210_epicoeff_IPDS11_100/epicoeff_IPDS11_100_hypercubeME.txt'



# hypercuboids_input = '211210_epicoeff_IPDS11_100/VZEM_dim2.txt'
# database_fitland_input = '211210_epicoeff_IPDS11_100_IPDS11_100.txt'
# output_epistatic_coefficients = '211210_epicoeff_IPDS11_100/epicoeff_IPDS11_100_hyperrectangles.txt'


import numpy as np, pandas as pd, time

# Triangular matrix
a = np.array(
	[
		[ 1,  0,  0, 0], 
		[-1,  1,  0, 0], 
		[-1,  0,  1, 0], 
		[ 1, -1, -1, 1]
	]
)


def main (hypercuboids_input, database_fitland_input, output_epistatic_coefficients):
	with open(hypercuboids_input, 'r') as input_hypercuboids, open(output_epistatic_coefficients, 'w') as output:
		start_time = time.time()
		# Read files, prepare output file
		input_hypercuboids.readline()
		input_fitland_df = pd.read_csv(database_fitland_input, delimiter='\t'); 
		input_fitland_df.rename(columns={ input_fitland_df.columns[0]: "mut_list" }, inplace=True); 
		input_fitland_df.rename(columns={ input_fitland_df.columns[1]: "fitness"  }, inplace=True)
		input_fitland_df['mut_list'] = input_fitland_df['mut_list'].fillna('0Z'); input_fitland_df.set_index('mut_list', inplace=True)
		if extended_output_flag == False:
			output.write("Hypercuboid_size" + '\t' + "a(wt)" + '\t' + "a(1)" + '\t' + "a(2)" + '\t' + "a(12)" + '\n')
		if extended_output_flag == True:
			output.write('diagonal' + '\t' + 'first_genotype' + '\t' + 'last_genotype' + '\t' + "Hypercuboid_size" + '\t' + "a(wt)" + '\t' + "a(1)" + '\t' + "a(2)" + '\t' + "a(12)" + '\t' + 'Type_of_epistasis' + '\n')
		# Start obtaining data
		for line in input_hypercuboids:
			# Each row -> list of items, each item - column
			line = line.strip(); line3 = line.split('\t'); 
			# fwt fitness
			fwt_seq = line3[2]; fwt = input_fitland_df.loc[fwt_seq, 'fitness']; 
			# print(f"fwt: {fwt_seq} {fwt}")
			# f12 fitness
			f12_seq  = line3[1]; f12 =  input_fitland_df.loc[f12_seq, 'fitness']; 
			# print(f"f12: {f12_seq} {f12}")
			# f1 fitness
			f1, size_f1 = construct_intermediate_sequences(fwt_seq, 'f1', line3, input_fitland_df)
			
			# f2 fitness
			f2, size_f2 = construct_intermediate_sequences(fwt_seq, 'f2', line3, input_fitland_df)

			total_size = size_f1 + size_f2
			
			b = [fwt, f1, f2, f12]
			c = a.dot(b)
			# print(c)
			if extended_output_flag == False: 
				output.write(str(total_size) + '\t' + str(c[0]) + '\t' + str(c[1]) + '\t' + str(c[2]) + '\t' + str(c[3]) + '\n')
			if extended_output_flag == True:
				# By default, no epistasis
				type_of_epistasis = 'no'
				delta_1 = f1 - fwt
				delta_2 = f2 - fwt
				delta_12 = f12 - f2
				delta_21 = f12 - f1
				# If c[3] (aka a(12)) is not zero, then there is some kind of non-additive effect:
				if c[3] != 0:
					type_of_epistasis = ''
					# Check for absence of sign or reciprocal sign epistasis
					if np.sign(delta_1) == np.sign(delta_12) and np.sign(delta_2) == np.sign(delta_21):
						# check positive epistasis condition:
						if fwt + delta_1 + delta_2 < f12:
							type_of_epistasis += 'positive;'
						# check negative epistasis
						elif fwt + delta_1 + delta_2 > f12:
							type_of_epistasis += 'negative;'
					# Sign epistasis
					elif np.sign(delta_1) == np.sign(delta_12) and np.sign(delta_2) != np.sign(delta_21) or np.sign(delta_2) == np.sign(delta_21) and np.sign(delta_1) != np.sign(delta_12):
						type_of_epistasis += 'sign;'
					# Reciprocal sign epistasis
					elif np.sign(delta_1) != np.sign(delta_12) and np.sign(delta_2) != np.sign(delta_21):
						type_of_epistasis += 'reciprocal_sign;'


				output.write(line3[0] +'\t' + line3[1] + '\t' + line3[2] + '\t' + str(total_size) + '\t' + str(c[0]) + '\t' + str(c[1]) + '\t' + str(c[2]) + '\t' + str(c[3]) + '\t' + type_of_epistasis + '\n')
		print(f'Program finished successfully! Runtime: {round(time.time() - start_time, 5)}')

def construct_intermediate_sequences(fwt_seq, fN, line3, input_fitland_df):
		list1 = []
		if ':' in fwt_seq:
			list1 = fwt_seq.split(':')
		else:
			list1.append(fwt_seq); 
		if fN == 'f1':
			mut1 = line3[0].split(':')[0]; 
		elif fN == 'f2':
			mut1 = line3[0].split(':')[1] 

		size1 = len(mut1.split(';'))
		for mut in mut1.split(';'):
			mut_int = str(mut[1:-1]) + str(mut[0]); list1.append(mut_int)
			# list1.append(mut[-2::-1])
		for item in list1:
			if item == '0Z':
				list1.remove(item)
		dict1 = dict()
		# print(list1)
		for i in list1:
			if int(i[:-1]) in dict1 and i[-1] == "Z":
				dict1.pop(int(i[:-1]))
			elif i[-1] != 'Z':
				dict1[int(i[:-1])] = i[-1]
		# print(dict1)
			# else:
				# dict1[i[:-1]] = i[-1]
		list2 = []
		for key, value in sorted(dict1.items()):
			list2.append(f"{key}{value}")
		fN_seq = ':'.join(list2)
		f_final = input_fitland_df.loc[fN_seq, 'fitness']
		# print(f"{fN}: {fN_seq} {f_final}")
		return f_final, size1


if __name__ == '__main__':
	#############################################################################################################################################################
	#####   Variables   #########################################################################################################################################
	#############################################################################################################################################################
	database_name = 'Khan_et_al_2011'
	sample_size = 32
	date = '220202'
	#############################################################################################################################################################
	print(f'Processing {database_name} {sample_size}...')

	##### hypercubes
	hypercuboids_input =            f'Epicoeff_{database_name}_{sample_size}_nonrand_{date}/hypercubes_2.txt'; 
	database_fitland_input =        f'Epicoeff_{database_name}_{sample_size}_nonrand_{date}/{database_name}_proc2_{sample_size}.txt'; 
	output_epistatic_coefficients = f'Epicoeff_{database_name}_{sample_size}_nonrand_{date}/epicoeff_{database_name}_{sample_size}_hypercubes.txt'
	main(hypercuboids_input, database_fitland_input, output_epistatic_coefficients)

	##### hyperrectangles
	hypercuboids_input =            f'Epicoeff_{database_name}_{sample_size}_nonrand_{date}/VZEM_dim2.txt'; 
	database_fitland_input =        f'Epicoeff_{database_name}_{sample_size}_nonrand_{date}/{database_name}_proc2_{sample_size}.txt'; 
	output_epistatic_coefficients = f'Epicoeff_{database_name}_{sample_size}_nonrand_{date}/epicoeff_{database_name}_{sample_size}_hyperrectangles.txt'
	main(hypercuboids_input, database_fitland_input, output_epistatic_coefficients)

