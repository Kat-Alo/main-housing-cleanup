import csv
import random
import sys


NUM_SPOTCHECK_DATA = 50


def generate_sample_csv(filename):

	with open(filename, 'r') as fr:
		headers = fr.readline()
		rows = fr.readlines()

	random.shuffle(rows)

	with open('data/processed/sample-original-data-spotcheck.csv', 'w') as original_f:
		original_f.write(headers)

		with open('data/processed/sample-processed-data-spotcheck.csv', 'w') as processed_f:
			processed_f.write(headers)

			original_counter = 0
			processed_counter = 0
			for row in rows:
				print(row)
				if original_counter == NUM_SPOTCHECK_DATA and processed_counter == NUM_SPOTCHECK_DATA:
					print("REACHED SAMPLE LIMIT FOR BOTH SEARCHES")
					break
				elif "false" in row and original_counter < NUM_SPOTCHECK_DATA:
					print("ADDING ROW FOR ORIGINAL DATA CHECK")
					print(row)
					original_f.write(row)
					original_counter += 1
				elif "true" in row and processed_counter < NUM_SPOTCHECK_DATA:
					print("ADDING ROW FOR PROCESSED DATA CHECK")
					print(row)
					processed_f.write(row)
					processed_counter += 1



if __name__ == '__main__':

	generate_sample_csv(sys.argv[1])