import csv
import sys


def main(big_filename, little_filename):

	with open(big_filename, 'r') as fr:
		headers = fr.readline()
		rows = fr.readlines()

	little_file1 = little_filename + "1" + ".csv"
	little_file2 = little_filename + "2" + ".csv"

	with open(little_file1, 'w') as fw1:
		fw1.write(headers)

		with open(little_file2, 'w') as fw2:
			fw2.write(headers)

			num_rows = len(rows)
			counter = 0

			for row in rows:
				if counter <= (num_rows/2):
					fw1.write(row)
					counter += 1
				else:
					fw2.write(row)



if __name__ == '__main__':
	
	main(sys.argv[1], sys.argv[2])