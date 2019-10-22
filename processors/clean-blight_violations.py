import csv
import sys
import datetime


NEW_CSV_HEADERS = ["ADDRESS", "HEARING DATE", "AMOUNT_DUE", "VIOLATION_DESCRIPTION"]


def is_after_today(hearing_date):
	today = datetime.datetime.now()

	if hearing_date != "":
		hearing_datetime = datetime.datetime.strptime(hearing_date, '%Y-%m-%d')

		if isinstance(hearing_datetime, datetime.datetime) and hearing_datetime >= today:

			return True
	
	return False

def is_current_balance(balance_due):

	balance_float = float(balance_due)

	if balance_float > 0:
		return True

	return False


def main(raw_filename, clean_filename):
	#create a reader for the raw blight violations csv
	with open(raw_filename) as fr:
		reader = csv.DictReader(fr)

		#create a writer for the final blight violations csv
		with open(clean_filename, 'w') as fw:
			writer = csv.writer(fw)

			#Write the new headers into the new CSV
			writer.writerow(NEW_CSV_HEADERS)

			for row in reader:
				new_row = []

				if is_after_today(row["hearing_date"].strip()[0:10]) or is_current_balance(row["balance_due"].strip()):
					new_row.append(row["violation_address"].strip().lower())
					new_row.append(row["hearing_date"].strip()[0:10])
					new_row.append(row["balance_due"])
					new_row.append(row["violation_description"])
					writer.writerow(new_row)



if __name__ == '__main__':

	main(sys.argv[1], sys.argv[2])





