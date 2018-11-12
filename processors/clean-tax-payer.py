import csv
import sys

DATE = "11082018"

NEW_CSV_HEADERS = ["ADDRESS", "TAXPAYER-OWNER"]
OLD_CSV_HEADERS = ["Address", "Owner"]

FINAL_CSV_FILENAME = 'data/processed/clean-tax-payer-' + DATE + '.csv'


def main(filename):
	#create a reader for the raw tax auction csv
	with open(filename) as fr:
		reader = csv.DictReader(fr)

		#create a writer for the final tax auction csv
		with open(FINAL_CSV_FILENAME, 'w') as fw:
			writer = csv.writer(fw)

			#Write the new headers into the new CSV
			writer.writerow(NEW_CSV_HEADERS)

			for row in reader:
				new_row = []

				for header in OLD_CSV_HEADERS:
					new_row.append(row[header])

				writer.writerow(new_row)


if __name__ == '__main__':

	main(sys.argv[1])