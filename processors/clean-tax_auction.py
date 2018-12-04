import csv
import sys


NEW_CSV_HEADERS = ["ADDRESS", "TAX-AUCTION-STATUS", "AMOUNT-DUE"]
OLD_CSV_HEADERS = ["address", "status", "due"]



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
				#This data is for all of Wayne County, but we just want Detroit
				if row['city'].strip() == 'detroit':
					
					new_row = []

					for header in OLD_CSV_HEADERS:
						new_row.append(row[header].lower())

					writer.writerow(new_row)


if __name__ == '__main__':

	main(sys.argv[1], sys.argv[2])