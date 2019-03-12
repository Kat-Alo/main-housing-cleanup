import csv
import sys
from datetime import date
from datetime import timedelta
import requests
import zipfile
import io

URL_ROOT = 'https://makeloveland.com/exports/taxes/'

#searches for most recent data scrape of Treasurer's tax statuses, conducted by Loveland
def main(data_dir):

	day = date.today()
	day_string = day.strftime("%Y%m%d")

	url = URL_ROOT + day_string + '.zip'

	zip_not_found = True

	while zip_not_found:	
		r = requests.get(url)
		#start with today
		try:
			z = zipfile.ZipFile(io.BytesIO(r.content))
			z.extractall(path=data_dir)
			zip_not_found = False
		#if that fails, work backwards
		except:
			day = day - timedelta(days=1)
			day_string = day.strftime("%Y%m%d")
			url = URL_ROOT + day_string + '.zip'

	#returning the date to track the date of tax status scrape conducted by Loveland
	print(day_string)
	return day_string


if __name__ == '__main__':
	main(sys.argv[1])