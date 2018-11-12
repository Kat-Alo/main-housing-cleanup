import csv
import sys
import re
import requests

from time import sleep

DATE = "11082018"

FINAL_CSV_FILENAME = 'data/processed/clean-zips-housing-' + DATE + '.csv'

VALID_ZIPCODES = [
	"48215", "48224", "48223", "48207", "48221", "48234", "48216", "48201", "48228", "48235", "48217",
	"48240", "48226", "48239", "48219", "48209", "48210", "48206", "48214", "48202", "48204", "48213",
	"48238", "48203", "48211", "48208", "48212", "48236", "48225", "48205", "48227"]

NEW_CSV_HEADERS = ["ADDRESS", "ZIP-CODE", "AUCTION-STATUS", "REGISTRATION", "FAILURE-COC", 
	"NUMBER-BLIGHT-TICKETS" , "OUTSTANDING-FINE", "LATITUDE", "LONGITUDE", "ZIP-MODIFIED", "CLEAN-ZIP-CODE"]

OLD_CSV_HEADERS = ["address", "zip code", "auction status", "registration", "failure to get coc", 
	"number of blight tickets", "outstanding fine"]

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'


def main(filename):
	#create a reader for the raw housing csv
	with open(filename) as fr:
		reader = csv.DictReader(fr)

		#create a writer for the final housing csv
		with open(FINAL_CSV_FILENAME, 'w') as fw:
			writer = csv.writer(fw)

			#Write the new headers into the new CSV
			writer.writerow(NEW_CSV_HEADERS)

			#go through and check each row
			for row in reader:

				#if the row has nothing, we are done. Please walk, don't run, to the exit.
				if row['address'].strip() == "":
					break

				#reset the list that will contain the new row to be written
				new_row = []

				#iterate over all the old headers with data we need and write that data into the row
				for header in OLD_CSV_HEADERS:
					new_row.append(row[header])

				#pull latitude from "location" value
				location = row["location"]
				lat_search = re.search('(?<=\()(.*?)(?=,)', location)
				lat = lat_search.group(0)
				new_row.append(lat)

				#pull longitude from "location" value
				lon_search = re.search('(?<=, )(.*?)(?=\))', location)
				lon = lon_search.group(0).strip()
				new_row.append(lon)

				#if the zip code is not one of the valid zip codes listed, we need to modify it and flag it as modified
				if row["zip code"] not in VALID_ZIPCODES:
					#indicate that the zip code was modified
					new_row.append("true")

					#'Okay, Google. What is the zip code for this address?'
					params = {
						'address' :  (row['address'] + " Detroit, MI"),
						'key' : GOOGLE_MAPS_API_KEY
					}

					req = requests.get(GOOGLE_MAPS_API_URL, params=params)
					res = req.json()

					#assumes first result is best result
					result = res['results'][0]

					address_components = result["address_components"]

					for component in address_components:
						if component['types'] and 'postal_code' in component.get('types'):
							new_zip = component["short_name"]
							break

					new_row.append(new_zip)

				else:
					#indicate that zip code was not modified
					new_row.append("false")

					#make new zip code same as original one
					new_row.append(row["zip code"])

				writer.writerow(new_row)
				print("NEW ROW HAS BEEN WRITTEN")
				print(new_row)

if __name__ == '__main__':

	main(sys.argv[1])
































