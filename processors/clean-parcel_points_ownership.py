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

NEW_CSV_HEADERS = ["ADDRESS", "ZIP-CODE", "PARCEL_POINTS_TAXPAYER", "PARCEL_POINTS_OWNER", "ZIP-MODIFIED", "CLEAN-ZIP-CODE"]

OLD_CSV_HEADERS = ["Address", "Zip Code", "Taxpayer", "Owner"]

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

GEOCODIO_ZIPS = 'data/static/geocodio-zip-codes.csv'


def get_zip_from_google(address):
	#'Okay, Google. What is the zip code for this address?'
	params = {
		'address' :  (address + " Detroit, MI"),
		'key' : os.getenv("GOOGLE_MAPS_API_KEY")
	}

	req = requests.get(GOOGLE_MAPS_API_URL, params=params)
	res = req.json()

	if len(res['results']) < 1:
		return "ERROR NO RESULTS FOUND FOR THIS ADDRESS"

	#assumes first result is best result
	result = res['results'][0]

	address_components = result["address_components"]

	for component in address_components:
		if component['types'] and 'postal_code' in component.get('types'):
			new_zip = component["short_name"]
			return new_zip
			break

	return "ERROR NO ZIP FOUND FOR ADDRESS"

#getting zip from CSV that came from geocodio processing Parcel Points Ownership, mid-March 2019
def get_zip_from_data(address):

	df = pd.read_csv(GEOCODIO_ZIPS, dtype=str)

	row = df[df['address']==address.upper()]

	item = row.iat[0,2]

	return item


def main(raw_filename, clean_filename):
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























