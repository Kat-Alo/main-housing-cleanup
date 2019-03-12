import csv
import random
import sys

def main(data_filename, spotcheck_filename, sample_size):

	sample_size = int(sample_size)

	with open(data_filename, 'r') as fr:
		headers = fr.readline()
		rows = fr.readlines()

	random.shuffle(rows)

	with open(spotcheck_filename, 'w') as fw:
		fw.write(headers)

		counter = 1

		for row in rows:
			if counter <= sample_size:
				fw.write(row)
				counter += 1
			else:
				break


#Written for special spotcheck where equal random sample was needed from two sources
def generate_sample_zip_csv(filename, sample_size):

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
				if original_counter == sample_size and processed_counter == sample_size:
					print("REACHED SAMPLE LIMIT FOR BOTH SEARCHES")
					break
				elif "false" in row and original_counter < sample_size:
					print("ADDING ROW FOR ORIGINAL DATA CHECK")
					print(row)
					original_f.write(row)
					original_counter += 1
				elif "true" in row and processed_counter < sample_size:
					print("ADDING ROW FOR PROCESSED DATA CHECK")
					print(row)
					processed_f.write(row)
					processed_counter += 1



if __name__ == '__main__':

	# generate_sample_csv(sys.argv[1], sys.argv[2])
	main(sys.argv[1], sys.argv[2], sys.argv[3])



