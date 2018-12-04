import csv
import sys
import datetime




NEW_CSV_HEADERS = ["ADDRESS", "HEARING DATE", "AMOUNT_DUE", "VIOLATION_DESCRIPTION"]


def is_after_today(hearing_date):
	today = datetime.datetime.now()

	if hearing_date != "":
		hearing_datetime = datetime.datetime.strptime(hearing_date, '%m/%d/%Y')

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

				if is_after_today(row["Hearing Date"].strip()) or is_current_balance(row["Balance Due"].strip()):
					new_row.append(row["Violation Address"].strip().lower())
					new_row.append(row["Hearing Date"])
					new_row.append(row["Balance Due"])
					new_row.append(row["Violation Description"])
					writer.writerow(new_row)


			


if __name__ == '__main__':

	main(sys.argv[1], sys.argv[2])



# new_csv_list = []

			# for row in reader:

			# 	new_row = []
			# 	address_already_entered = False

			# 	if row["Balance Due"].strip() != "$0.00" or is_after_today(row["Hearing Date"]):

			# 		address = row["Violation Street Number"] + " " + row["Violation Street Name"]

			# 		if len(new_csv_list) > 0:
			# 			for item in new_csv_list:
			# 				if item[0].strip() == address.strip():
			# 					item[1] += 1
			# 					address_already_entered = True
			# 					break

			# 		if address_already_entered == False:
			# 			new_row.append(address)
			# 			new_row.append(1)
			# 			new_csv_list.append(new_row)

			# for item in new_csv_list:	
			# 	writer.writerow(item)











