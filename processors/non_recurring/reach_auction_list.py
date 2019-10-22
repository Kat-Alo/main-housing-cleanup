import csv
import pandas as pd

HEADERS = ['address', 'auction_status']

PARCEL_POINTS_FILENAME = 'data/raw/08222019/raw-parcel_points_ownership.csv'
AUCTION_FILENAME = 'data/static/wayne_county_auction_list_08192019/merged_auction_list_split_addresses.csv'

def get_auction_data():

	auction_data = {}

	with open(AUCTION_FILENAME) as auction_f:
		auction_reader = csv.DictReader(auction_f)

		for row in auction_reader:

			auction_data[row['address']] = [row['status'], row['minimum_bid_closing_time_ET'], row['city']]

	return auction_data

def auction_message(address, auction_data):

	if address in auction_data.keys() and auction_data[address][2].strip().upper() == 'DETROIT' and auction_data[address][0].strip().upper() == 'ACTIVE':
		return "{address} is on the Wayne County auction list as of Aug. 20, 2019. The minimum bid is ${min_bid}.".format(address=address, status=auction_data[address][0], min_bid=auction_data[address][1])

	elif address in auction_data.keys() and auction_data[address][2].strip().upper() == 'DETROIT':
		return "{address} is on the Wayne County auction list as of Aug. 20, 2019, however the status is {status}.".format(address=address, status=auction_data[address][0], min_bid=auction_data[address][1])

	else:
		return "{address} was not on the Wayne County auction list as of Aug. 20, 2019.".format(address=address)

def main():

	with open('data/static/wayne_county_auction_list_08192019/reach_auction_list.csv', 'w') as f:

		writer = csv.writer(f)
		writer.writerow(HEADERS)

		with open(PARCEL_POINTS_FILENAME) as parcel_f:
			parcel_reader = csv.DictReader(parcel_f)

			auction_data = get_auction_data()

			counter = 0

			for row in parcel_reader:

				new_row = []
				new_row.append(row['Address'])
				new_row.append(auction_message(row['Address'], auction_data))
				if "status" in auction_message(row['Address'], auction_data):
					counter += 1
				writer.writerow(new_row)

			print(counter)


if __name__ == '__main__':
	main()