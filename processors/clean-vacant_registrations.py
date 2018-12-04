import csv
import sys


NEW_CSV_HEADERS = ["ADDRESS", "VACANT-REGISTERED-FIRST-NAME", "VACANT-REGISTERED-LAST-NAME"]
OLD_CSV_HEADERS = ["Address", "First Name", "Last Name"]



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

				writer.writerow(new_row)


if __name__ == '__main__':

	main(sys.argv[1], sys.argv[2])