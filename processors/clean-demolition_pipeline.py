import csv
import sys


NEW_CSV_HEADERS = ["ADDRESS", "DEMOLITION-PIPELINE"]
OLD_CSV_HEADERS = ["\ufeffAddress"]


def main(raw_filename, clean_filename):
	#create a reader for the raw tax auction csv
	with open(raw_filename) as fr:
		reader = csv.DictReader(fr)

		#create a writer for the final tax auction csv
		with open(clean_filename, 'w') as fw:
			writer = csv.writer(fw)

			#Write the new headers into the new CSV
			writer.writerow(NEW_CSV_HEADERS)

			for row in reader:
				new_row = []

				for header in OLD_CSV_HEADERS:
					new_row.append(row[header].strip().lower())

				new_row.append("true")

				writer.writerow(new_row)


if __name__ == '__main__':

	main(sys.argv[1], sys.argv[2])
