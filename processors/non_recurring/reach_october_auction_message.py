import csv
import pandas as pd

HEADERS = ['address', 'auction_status']

PARCEL_POINTS_FILENAME = 'data/raw/10212019/raw-parcels.csv'
SEPT_AUCTION_FILENAME = 'data/static/wayne_county_auction_list_08192019/merged_auction_list_split_addresses.csv'
OCT_AUCTION_FILENAME = 'data/static/wayne_county_auction_list_10152019/merged_auction_list_split_addresses.csv'
REACH_MESSAGE_FILENAME = 'data/static/wayne_county_auction_list_10152019/reach_auction_list.csv'

def get_auction_data(filename):

	auction_data = {}

	with open(filename) as auction_f:
		auction_reader = csv.DictReader(auction_f)

		for row in auction_reader:

			auction_data[row['address']] = [row['status'], row['minimum_bid_closing_time_ET'], row['city']]

	return auction_data

def address_on_both_lists(address, sept_auction_data, oct_auction_data):

	if address in sept_auction_data.keys() and address in oct_auction_data.keys() and oct_auction_data[address][0].strip().upper() == 'ACTIVE':
		return True

	return False

def address_on_list(address, auction_data):

	if address in auction_data.keys():
		return True

	return False

def address_removed_from_auction(address, auction_data):

	if address in auction_data.keys() and auction_data[address][0].strip().upper() == 'REMOVED FROM AUCTION':
		return True

	return False

def auction_message(address, sept_auction_data, oct_auction_data):

	#on both lists and most recently has been active
	if address_on_both_lists(address, sept_auction_data, oct_auction_data):
		return "{address} was not sold at the Sept auction, so it is currently in the Oct auction for ${min_bid}.".format(address=address, min_bid=oct_auction_data[address][1])
	
	#only on september
	elif address_on_list(address, sept_auction_data):
		return "{address} was on the Sept auction list, but is not on the Oct list, which means it was either sold or removed from auction.".format(address=address)

	#only on october and active
	elif address_on_list(address, oct_auction_data) and oct_auction_data[address][0].strip().upper() == 'ACTIVE':
		return "{address} was not on the Sept auction list, but it has been added to the Oct auction for ${min_bid}.".format(address=address, min_bid=oct_auction_data[address][1])

	elif address_removed_from_auction(address, oct_auction_data):
		return "{address} was on the October auction list, however it was removed from auction.".format(address=address)

	else:
		return "{address} was not on the list for either the September or October Wayne County tax auction.".format(address=address)

def main():

	with open(REACH_MESSAGE_FILENAME, 'w') as f:

		writer = csv.writer(f)
		writer.writerow(HEADERS)

		with open(PARCEL_POINTS_FILENAME) as parcel_f:
			parcel_reader = csv.DictReader(parcel_f)

			sept_auction_data = get_auction_data(SEPT_AUCTION_FILENAME)
			oct_auction_data = get_auction_data(OCT_AUCTION_FILENAME)

			counter = 0

			for row in parcel_reader:

				new_row = []
				new_row.append(row['ADDRESS'])
				new_row.append(auction_message(row['ADDRESS'], sept_auction_data, oct_auction_data))
				writer.writerow(new_row)


if __name__ == '__main__':
	main()


