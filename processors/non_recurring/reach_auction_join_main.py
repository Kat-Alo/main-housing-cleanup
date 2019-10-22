import pandas as pd 


AUCTION_FILENAME = 'data/static/wayne_county_auction_list_10152019/reach_auction_list.csv'
MAIN_REACH_FILENAME = 'data/processed/10212019/reach_webhook.csv'
FINAL_FILENAME = 'data/static/wayne_county_auction_list_10152019/main_reach_with_auction.csv'


def main():

	auction_data = pd.read_csv(AUCTION_FILENAME)
	main_reach_data = pd.read_csv(MAIN_REACH_FILENAME)

	merged_data = pd.merge(main_reach_data, auction_data, on='address')

	merged_data.to_csv(FINAL_FILENAME)


if __name__ == '__main__':
	main()