import csv
import sys
import re
import requests
import os
import pandas as pd


VALID_ZIPCODES = [
	"48215", "48224", "48223", "48207", "48221", "48234", "48216", "48201", "48228", "48235", "48217",
	"48240", "48226", "48239", "48219", "48209", "48210", "48206", "48214", "48202", "48204", "48213",
	"48238", "48203", "48211", "48208", "48212", "48236", "48225", "48205", "48227"]

NEW_CSV_HEADERS = ["ADDRESS", "ZIP-CODE", "PARCEL_POINTS_TAXPAYER", "PARCEL_POINTS_OWNER", "PARCEL_POINTS_PRE", "ZIP-MODIFIED", "CLEAN-ZIP-CODE", "CORRECTED_PRE", "PRE_SAME"]

OLD_CSV_HEADERS = ["Address", "Zip Code", "Taxpayer", "Owner", "Principal Residence Exemption"]

GEOCODIO_ZIPS = 'data/static/geocodio-zip-codes.csv'

CORRECTED_PRE_FILENAME = 'data/static/corrected_assessor_parcel_received_060819.csv'

#getting zip from CSV that came from geocodio processing Parcel Points Ownership, mid-March 2019
def get_zip_from_data(address):

	df = pd.read_csv(GEOCODIO_ZIPS, dtype=str)

	row = df[df['address']==address.upper()]

	item = row.iat[0,2]

	return item

def is_row_empty(row):

	for key in row.keys():
		if row[key].strip() != "":
			return False

	return True

def add_zip_values(row, new_row):
	#if the zip code is not one of the valid zip codes listed, we need to modify it and flag it as modified
	if row["Zip Code"] not in VALID_ZIPCODES and row['Address'].strip() != "":
		#indicate that the zip code was modified
		new_row.append("true")

		new_zip = get_zip_from_data(row['Address'])

		new_row.append(new_zip)

	elif row['Address'].strip() == "":
		new_row.append("N/A")
		new_row.append("N/A")

	else:
		#indicate that zip code was not modified
		new_row.append("false")

		#make new zip code same as original one
		new_row.append(row["Zip Code"])

	return new_row

def add_pre_values(new_row, data):

	if data.get(new_row[0].strip().upper()):
		
		new_row.append(data[new_row[0].strip().upper()])

	else:
		new_row.append("ADDRESS NOT FOUND")

	if new_row[4].strip().upper() == new_row[7].strip().upper():
		new_row.append("True")
	else:
		new_row.append("False")

	return new_row

def get_corrected_pre_data():

	data = {}

	with open(CORRECTED_PRE_FILENAME, encoding="ISO-8859-1") as f:

		reader = csv.DictReader(f)

		for row in reader:

			data[row['PropertyAddressCombined']] = row['ParcelsMayPRE']

	return data

def main(raw_filename, clean_filename):

	corrected_pre_data = get_corrected_pre_data()

	#create a reader for the raw housing csv
	with open(raw_filename) as fr:
		reader = csv.DictReader(fr)

		#create a writer for the final housing csv
		with open(clean_filename, 'w') as fw:
			writer = csv.writer(fw)

			#Write the new headers into the new CSV
			writer.writerow(NEW_CSV_HEADERS)

			counter = 0

			#go through and check each row
			for row in reader:

				row_empty = True

				for key in row.keys():
					if row[key].strip() != "":
						row_empty = False
						break

				#if the row has nothing, we are done. Please walk, don't run, to the exit.
				if row_empty:
					break

				#reset the list that will contain the new row to be written
				new_row = []

				#iterate over all the old headers with data we need and write that data into the row
				for header in OLD_CSV_HEADERS:
					new_row.append(row[header].strip().lower())

				#if the zip code is not one of the valid zip codes listed, we need to modify it and flag it as modified
				if row["Zip Code"] not in VALID_ZIPCODES and row['Address'].strip() != "":
					#indicate that the zip code was modified
					new_row.append("true")

					# print("Zip code %s not valid" % row["Zip Code"])

					new_zip = get_zip_from_data(row['Address'])

					new_row.append(new_zip)

				elif row['Address'].strip() == "":

					new_row.append("N/A")
					new_row.append("N/A")

				else:
					#indicate that zip code was not modified
					new_row.append("false")

					#make new zip code same as original one
					new_row.append(row["Zip Code"])

				writer.writerow(new_row)
				# print("Row written for address: %s" % new_row[0])

				counter += 1

if __name__ == '__main__':

	main(sys.argv[1], sys.argv[2])























