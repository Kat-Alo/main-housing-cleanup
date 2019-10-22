import csv
import sys


NEW_CSV_HEADERS = ["ADDRESS", "VACANT-CERTIFIED-FIRST-NAME", "VACANT-CERTIFIED-LAST-NAME"]
OLD_CSV_HEADERS = ["address", "csm_name_first", "csm_name_last"]


def main(raw_filename, clean_filename):
	#create a reader for the raw vacant certifications csv
	with open(raw_filename) as fr:
		reader = csv.DictReader(fr)

		#create a writer for the final vacant certifications csv
		with open(clean_filename, 'w') as fw:
			writer = csv.writer(fw)

			#Write the new headers into the new CSV
			writer.writerow(NEW_CSV_HEADERS)

			for row in reader:
				new_row = []

				for header in OLD_CSV_HEADERS:
					new_row.append(row[header].strip().lower())

				writer.writerow(new_row)


if __name__ == '__main__':

	main(sys.argv[1], sys.argv[2])