import xlrd
import csv
import os
import pandas as pd
import logging

XLS_DIRECTORY = "data/static/wayne_county_auction_list_10152019/xls"
CSV_DIRECTORY = "data/static/wayne_county_auction_list_10152019/csv"
AUCTION_DIRECTORY = "data/static/wayne_county_auction_list_10152019"

FINAL_HEADERS = ["auction_item_ID", "address", "city", "zip", "parcel_ID", "minimum_bid_closing_time_ET", "closing_time", "status", "summer_tax", "zoning"]

def convert_to_csv(xls_filename, counter):

	csv_filename = 'auction_list_' + str(counter) + '.csv'

	csv_path = os.path.join(CSV_DIRECTORY, csv_filename)

	logging.info("Converting {xls} to CSV".format(xls=xls_filename))

	data_list = pd.read_html(xls_filename, header=0)
	data = data_list[0]

	data.to_csv(csv_path, index=False)

def split_address_fields(merged_csv):

	with open(merged_csv) as fr:
		reader = csv.reader(fr)
		#skip the header
		next(reader)
		with open(os.path.join(AUCTION_DIRECTORY,'merged_auction_list_split_addresses.csv'), 'w') as fw:

			writer = csv.writer(fw)
			writer.writerow(FINAL_HEADERS)

			for row in reader:
				new_row = []
				new_row.append(row[0])

				split_address = row[1].split(',')

				address = split_address[0].upper()
				if "DETROIT" in address:
					address = address.replace("DETROIT", "")

				new_row.append(address)

				city = split_address[1].upper()

				if "CITY OF " in city:
					city = city.replace("CITY OF ", "")

				new_row.append(city)
				new_row.append(split_address[2])

				for i in row[2:]:
					new_row.append(i)

				writer.writerow(new_row)

def main():

	counter = 0
	for file in os.listdir(XLS_DIRECTORY):
	    if file.endswith(".xls"):
	    	counter += 1
	    	path = os.path.join(XLS_DIRECTORY, file)
	    	convert_to_csv(path, counter)

	csv_files = []
	counter = 0
	for file in os.listdir(CSV_DIRECTORY):
		if file.endswith(".csv"):

			csv_files.append(pd.read_csv(os.path.join(CSV_DIRECTORY, file)))

	merged = pd.concat(csv_files)
	merged.to_csv(os.path.join(AUCTION_DIRECTORY,'merged_auction_list.csv'), index=None)

	split_address_fields(os.path.join(AUCTION_DIRECTORY,'merged_auction_list.csv'))

if __name__ == '__main__':
	main()