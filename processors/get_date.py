import datetime

def main():

	today = datetime.date.today().strftime("%m%d%Y")
	print(today)

if __name__ == '__main__':
	main()