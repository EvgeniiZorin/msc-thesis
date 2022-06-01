import unittest
import io
import os
import Epistatic_coefficients_calculator

class TestEpistaticCoefficients(unittest.TestCase):
	def test_if_equal_hyperrectangles(self):
		"""
		hyperrectangles <- VZEM_hypercuboids.py
		test_complete_03.txt
		"""
		# Run for hyperrectangles: 
		hypercuboids_input = 'test_functional/VZEM_dim2.txt'; database_fitland_input = 'test_functional/test_complete_03.txt'; output_epistatic_coefficients = 'test_epistatic_coefficients_hyperrectangles.txt'
		Epistatic_coefficients_calculator.main(hypercuboids_input, database_fitland_input, output_epistatic_coefficients)
		with io.open('test_functional/Epistatic_coefficients_standard_hyperrectangles.txt') as open, io.open('test_epistatic_coefficients_hyperrectangles.txt') as open2: 
			self.assertListEqual(list(open), list(open2))
	def test_if_equal_hypercubes(self):
		"""
		hypercubes <- hypercubeME.py
		test_complete_03.txt
		"""
		# Run for hypercubes:
		hypercuboids_input = 'test_functional/hypercubes_2.txt'; database_fitland_input = 'test_functional/test_complete_03.txt'; output_epistatic_coefficients = 'test_epistatic_coefficients_hypercubeME.txt'
		Epistatic_coefficients_calculator.main(hypercuboids_input, database_fitland_input, output_epistatic_coefficients)
		with io.open('test_functional/Epistatic_coefficients_standard_hypercubeME.txt') as open, io.open('test_epistatic_coefficients_hypercubeME.txt') as open2:
			self.assertListEqual(list(open), list(open2))
	def test_if_equal_hyperrectangles2(self):
		"""
		hyperrectangles created manually
		fitland database created manually
		"""
		hypercuboids_input = 'test_functional/custom_hyperrectangles.txt'; database_fitland_input = 'test_functional/custom_dataset.txt'; output_epistatic_coefficients = 'test_epicoeff_hyperrect_custom.txt'
		Epistatic_coefficients_calculator.main(hypercuboids_input, database_fitland_input, output_epistatic_coefficients)
		with io.open('test_functional/Epistatic_coefficients_standard_customdatabase.txt') as open, io.open('test_epicoeff_hyperrect_custom.txt') as open2:
			self.assertListEqual(list(open), list(open2))


if __name__=='__main__':
	# if not os.path.exists('test_epistatic_coefficients_hyperrectangles.txt'):
	# 	raise Exception("Output with epistatic coefficients doesn't exist! \n Please run main script 'Epistatic_coefficients_calculator.py': \n   - input file: Unittest/test_complete_03.txt \n   - input file 2: Unittest/VZEM_dim2.txt \n   - output file name: test_epistatic_coefficients.txt \nand then run this unittest again :)")
	try: 
		unittest.main()
	except FileNotFoundError:
		print("One of the files not found!")

	# else:
	# 	unittest.main()