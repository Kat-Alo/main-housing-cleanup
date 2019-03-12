import csv
import sys
import datetime

# NEW_CSV_HEADERS = ["address", "rental_reg_status", "number_blight_tickets", "coc_date", "tax_auction_status",
# 	"amount_due", "taxpayer", "owner", "demolition_status", "vacant_status", "dlba_inventory_status"]

NEW_CSV_HEADERS = ["address", "Q1_tax_status", "Q2_rental_reg_status", "Q3_vacant_concern", "Q4_vacant_purchase"]

STREET_ABBREVIATIONS = ["st", "blvd", "ct", "dr", "ave", "ctr", "cir", "hwy", "jct", "ln", "pkwy", "rd"]

COC_DATES_BY_ZIP = {"48215": "now", "48224": "now", "48223": "now", "48207": "by Sept 1, 2019", 
	"48221": "by Sept 1, 2019", "48234": "by Oct 1, 2019", "48216": "by Oct 1, 2019", "48201": "by Nov 1, 2019",
	"48228": "by Nov 1, 2019", "48235": "by Dec 1, 2019", "48217": "by Dec 1, 2019", "48240": "by Jan 1, 2020",
	"48226": "by Jan 1, 2020", "48239": "by Jan 1, 2020", "48219": "by Dec 1, 2018", "48209": "by Jan 1, 2019",
	"48210": "by Feb 1, 2019", "48206": "by Mar 1, 2019", "48214": "by Mar 1, 2019", "48202": "by Apr 1, 2019",
	"48204": "by Apr 1, 2019", "48213": "by May 1, 2019", "48238": "by May 1, 2019", "48203": "by Jun 1, 2019",
	"48211": "by Jun 1, 2019", "48208": "by July 1, 2019", "48212": "by July 1, 2019", "48236": "by Aug 1, 2019",
	"48225": "by Aug 1, 2019", "48205": "by Aug 1, 2019", "48227": "by Aug 1, 2019"}


def process_rental_reg_status(rental_reg_status):

	if rental_reg_status.strip() == "vio":
		new_status = "The city has issued a rental registration violation for this property"
	elif rental_reg_status.strip() == "emg":
		new_status = "This property has been flagged as an emergency demolition or violation"
	elif rental_reg_status.strip() == "ins":
		new_status = "This property has been inspected by the city as part of the rental registration process"
	elif rental_reg_status.strip() == "coc":
		new_status = "This property has been inspected by the city and has a certificate of compliance"
	elif rental_reg_status.strip() == "dah":
		new_status = "This property is undergoing hearings as part of the rental registration process"
	elif rental_reg_status.strip() == "wal":
		new_status = "This property is listed by the city as having a wall issue"
	elif rental_reg_status.strip() == "":
		new_status = "This property is not registered as a rental with the city"
	elif rental_reg_status.strip() == "rtm":
		new_status = "This property is not yet registered with the city as a rental b/c of a mail issue"
	elif rental_reg_status.strip() == "reg":
		new_status = "This property is registered with the city as a rental but still needs to be inspected"
	else:
		new_status = "This property's rental registration status listed by the city is: %s" % rental_reg_status.upper()

	return new_status

def process_number_blight_tickets(number_blight_tickets):

	if number_blight_tickets == "":
		return "zero"

	return number_blight_tickets

def process_coc_date(zip_code):

	if zip_code in COC_DATES_BY_ZIP.keys():
		return "All rentals in that zip code need to be registered and inspected with the city by %s" % COC_DATES_BY_ZIP[zip_code]		 
	else:
		return "This zip code does not have a rental compliance date"

def process_taxpayer(taxpayer):

	return taxpayer.upper()

def process_owner(owner):

	return owner.upper()

def process_demolition_status(demolition_date, demolition_pipeline):

	demolition_status = ""

	today = datetime.datetime.now()
	year_from_now = today + datetime.timedelta(days=365)

	year_from_now_string = year_from_now.strftime("%m-%d-%Y")

	if demolition_date.strip() != "":
		demolition_status = "This property is on the city's demolition list, and is set to be demolished by %s" % demolition_date
	elif demolition_pipeline.strip() != "":
		demolition_status = "The city says it will schedule this property for demolition by %s" % year_from_now_string
	else:
		demolition_status = "This property is not on the city's demolition list"
	return demolition_status

def process_vacant_status(certified, registered):

	if certified.strip() != "":
		vacant_status = "This property is has been certified as a vacant property (meaning it was registered by the owner and inspected by the city)"
	elif registered.strip() != "":
		vacant_status = "This property is registered as vacant, but hasn't been inspected/certified yet"
	else:
		vacant_status = "This property is not registered as vacant"

	return vacant_status

def process_dlba_inventory_status(inventory_status):

	if inventory_status.strip() == "dlba owned sidelot for sale" or inventory_status.strip() == "dlba owned structure for sale":
		new_inventory_status = "This property is owned by the Land Bank and is for sale"
	elif inventory_status.strip() == "dlba owned structure" or inventory_status.strip() == "dlba owned vacant land":
		new_inventory_status = "This property is owned by the Land Bank and is not for sale"
	else:
		new_inventory_status = "This property is not owned by the Land Bank"

	return new_inventory_status

def process_vacant_concern_message(row):

	taxpayer = process_taxpayer(row['taxpayer'])
	address = process_address(row['address'])
	demolition_status = process_demolition_status(row['projected_demolish_by_date'], row['demolition_pipeline'])
	number_blight_tickets = process_number_blight_tickets(row['number_blight_tickets'])

	if number_blight_tickets.isdigit() and int(number_blight_tickets) == 1:
		return "The city has {taxpayer} listed as the taxpayer for {address}. {demolition_status}. There is {number_blight_tickets} open blight ticket for that address.".format(taxpayer=taxpayer,
			address=address, demolition_status=demolition_status, number_blight_tickets=number_blight_tickets)

	return "The city has {taxpayer} listed as the taxpayer for {address}. {demolition_status}. There are {number_blight_tickets} open blight tickets for that address.".format(taxpayer=taxpayer,
		address=address, demolition_status=demolition_status, number_blight_tickets=number_blight_tickets)

def process_rental_message(row):

	taxpayer = process_taxpayer(row['taxpayer'])
	address = process_address(row['address'])
	rental_reg_status = process_rental_reg_status(row['rental_reg_status'])
	coc_date = process_coc_date(row['zip_code'])

	return "{taxpayer} is listed as the taxpayer for {address}. {rental_reg_status}. {coc_date}.".format(taxpayer=taxpayer, address=address, rental_reg_status=rental_reg_status,
		coc_date=coc_date)

def process_tax_message(row):

	taxpayer = process_taxpayer(row['taxpayer'])
	address = process_address(row['address'])
	tax_auction_status = row['tax_auction_status'].strip()
	amount_due = row['amount_due'].strip()

	if tax_auction_status == "":
		return "{taxpayer} is listed as the taxpayer for {address}. There is no overdue tax debt listed for this property".format(taxpayer=taxpayer, address=address)

	elif amount_due.strip() == "":
		return "{taxpayer} is listed as the taxpayer for {address}. This property has been foreclosed".format(taxpayer=taxpayer, address=address)

	return "{taxpayer} is listed as the taxpayer for {address}. The tax status is {tax_auction_status} and the tax due is ${amount_due}".format(taxpayer=taxpayer,
		address=address, tax_auction_status=tax_auction_status, amount_due=amount_due)


def process_address(address):
	split_address = address.split(" ")

	if split_address[-1] in STREET_ABBREVIATIONS:
		split_address.pop()

	new_address = " ".join(split_address)

	return new_address.upper().strip()

def row_is_complete(row):

	count_values = 0

	for header in row.keys():
		if row[header].strip() != "":
			count_values += 1

	if count_values > 2:
		return True

	return False

def main(overview_filename, groundsource_filename):

	#create a reader for the raw overview file
	with open(overview_filename) as fr:
		reader = csv.DictReader(fr)

		#create a writer for the final groundsource csv
		with open(groundsource_filename, 'w') as fw:
			writer = csv.writer(fw)

			#Write the new headers into the new CSV
			writer.writerow(NEW_CSV_HEADERS)

			for row in reader:
				new_row = []

				if row_is_complete(row):

					new_row.append(process_address(row['address']))
					new_row.append(process_tax_message(row))
					new_row.append(process_rental_message(row))
					new_row.append(process_vacant_concern_message(row))
					new_row.append(process_dlba_inventory_status(row['inventory_status']))

					writer.writerow(new_row)



if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])


