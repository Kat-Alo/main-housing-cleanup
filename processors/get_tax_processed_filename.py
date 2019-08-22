import sys

def extract_date(raw_filename):

	return raw_filename[0:8]
	

def main(raw_filename):

	tax_scrape_date = extract_date(raw_filename)

	print("tax_data_" + tax_scrape_date + ".csv")


if __name__ == '__main__':
	main(sys.argv[1])