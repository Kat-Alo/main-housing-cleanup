import sys
import csv


OLD_CSV_HEADERS = ["ADDRESS", "ZIP-CODE", "REGISTRATION", "FAILURE-COC", 
	"NUMBER-BLIGHT-TICKETS" , "OUTSTANDING-FINE", "LATITUDE", "LONGITUDE", "ZIP-MODIFIED", "CLEAN-ZIP-CODE"]

NEW_CSV_HEADERS = ["ADDRESS", "ZIP-CODE", "RENTAL_REG_STATUS", "FAILURE-COC", 
	"NUMBER-BLIGHT-TICKETS" , "OUTSTANDING-FINE", "LATITUDE", "LONGITUDE", "ZIP-MODIFIED", "CLEAN-ZIP-CODE"]



def main(raw_filename, clean_filename):

	with open(raw_filename) as fr:
		reader = csv.DictReader(fr)

		with open(clean_filename, 'w') as fw:
			writer = csv.writer(fw)

			#Write the new headers into the new CSV
			writer.writerow(NEW_CSV_HEADERS)

			for row in reader:
				new_row = []
				
				for header in OLD_CSV_HEADERS:
					new_row.append(row[header].lower())

				writer.writerow(new_row)








if __name__ == '__main__':

	main(sys.argv[1], sys.argv[2])