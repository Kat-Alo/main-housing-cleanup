import datetime
import logging

from os import listdir
from os.path import isfile, join

RAW_DIRECTORY_ROOT = 'data/raw/'

def main():

	today = datetime.date.today().strftime("%m%d%Y")
	raw_directory = RAW_DIRECTORY_ROOT + today

	files = [f for f in listdir(raw_directory) if isfile(join(raw_directory, f))]

	if '.DS_Store' in files: files.remove('.DS_Store')

	if len(files) == 0:
		logging.error("There aren't any files in the raw directory. Move the raw tax data there.")

	elif len(files) > 1:
		logging.error("There are multiple files in the raw directory. Make sure the raw tax data is the only file present.")

	else:
		print(files[0])


if __name__ == '__main__':
	main()