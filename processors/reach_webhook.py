import csv
import sys
import datetime

# NEW_CSV_HEADERS = ["address", "rental_reg_status", "number_blight_tickets", "coc_date", "tax_auction_status",
# 	"amount_due", "taxpayer", "owner", "demolition_status", "vacant_status", "dlba_inventory_message"]

NEW_CSV_HEADERS = ["address", "Q1_tax_status", "Q2_rental_reg_status", "Q3_vacant_concern", "Q4_vacant_purchase", "Q5_pre"]

STREET_ABBREVIATIONS = ["st", "blvd", "ct", "dr", "ave", "ctr", "cir", "hwy", "jct", "ln", "pkwy", "rd"]

COC_DATES_BY_ZIP = {"48215": datetime.datetime(2018, 8, 1), "48224": datetime.datetime(2018, 9, 1), "48223": datetime.datetime(2019, 1, 2), "48207": datetime.datetime(2020, 9, 1), 
	"48221": datetime.datetime(2020, 9, 1), "48234": datetime.datetime(2020, 10, 1), "48216": datetime.datetime(2020, 10, 1), "48201": datetime.datetime(2021, 1, 2),
	"48228": datetime.datetime(2021, 1, 2), "48235": datetime.datetime(2021, 2, 1), "48217": datetime.datetime(2021, 2, 1), "48240": datetime.datetime(2021, 5, 1),
	"48226": datetime.datetime(2021, 5, 1), "48239": datetime.datetime(2021, 5, 1), "48219": datetime.datetime(2019, 2, 1), "48209": datetime.datetime(2019, 5, 1),
	"48210": datetime.datetime(2019, 6, 3), "48206": datetime.datetime(2019, 9, 3), "48214": datetime.datetime(2019, 9, 3), "48202": datetime.datetime(2019, 10, 1),
	"48204": datetime.datetime(2019, 10, 1), "48213": datetime.datetime(2020, 1, 2), "48238": datetime.datetime(2019, 1, 2), "48203": datetime.datetime(2020, 2, 1),
	"48211": datetime.datetime(2020, 2, 1), "48208": datetime.datetime(2020, 5, 1), "48212": datetime.datetime(2020, 5, 1), "48236": datetime.datetime(2020, 6, 1),
	"48225": datetime.datetime(2020, 6, 1), "48205": datetime.datetime(2020, 6, 1), "48227": datetime.datetime(2020, 6, 1)}


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

	#if the compliance date has already passed
	if zip_code in COC_DATES_BY_ZIP.keys() and COC_DATES_BY_ZIP[zip_code] < datetime.datetime.now():
		return "All rentals in that zip code should have been registered and inspected with the city by %s" % COC_DATES_BY_ZIP[zip_code].strftime("%d %b, %Y")		 
	#if the compliance date is in the future
	elif zip_code in COC_DATES_BY_ZIP.keys():
		return "All rentals in that zip code should be registered and inspected with the city by %s" % COC_DATES_BY_ZIP[zip_code].strftime("%d %b, %Y")
	#if the zip is one of the few that isn't actually a Detroit zip code
	else:
		return "This zip code does not have a rental compliance date"

def process_taxpayer(row):

	if row['taxpayer'].strip() != "":
		return row['taxpayer'].upper()

	else:
		return row['parcels_taxpayer'].upper()

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

def process_dlba_inventory_message(row):

	inventory_status = row['inventory_status']
	address = process_address(row['address'])

	if inventory_status.strip() == "dlba owned sidelot for sale" or inventory_status.strip() == "dlba owned structure for sale":
		new_inventory_status = "{address} is owned by the Land Bank and is for sale".format(address=address)
	elif inventory_status.strip() == "dlba owned structure" or inventory_status.strip() == "dlba owned vacant land":
		new_inventory_status = "{address} is owned by the Land Bank and is not for sale".format(address=address)
	else:
		new_inventory_status = "{address} is not owned by the Land Bank".format(address=address)

	return new_inventory_status

def process_vacant_concern_message(row):

	taxpayer = process_taxpayer(row)
	address = process_address(row['address'])
	demolition_status = process_demolition_status(row['projected_demolish_by_date'], row['demolition_pipeline'])
	number_blight_tickets = process_number_blight_tickets(row['number_blight_tickets'])

	if number_blight_tickets.isdigit() and int(number_blight_tickets) == 1:
		return "{taxpayer} is listed as the taxpayer for {address}. {demolition_status}. There is {number_blight_tickets} open blight ticket for that address.".format(taxpayer=taxpayer,
			address=address, demolition_status=demolition_status, number_blight_tickets=number_blight_tickets)

	return "{taxpayer} is listed as the taxpayer for {address}. {demolition_status}. There are {number_blight_tickets} open blight tickets for that address.".format(taxpayer=taxpayer,
		address=address, demolition_status=demolition_status, number_blight_tickets=number_blight_tickets)

def process_rental_message(row):

	taxpayer = process_taxpayer(row)
	address = process_address(row['address'])
	rental_reg_status = process_rental_reg_status(row['rental_reg_status_historic'])
	coc_date = process_coc_date(row['zip_code'])

	return "{taxpayer} is listed as the taxpayer for {address}. {rental_reg_status}. {coc_date}.".format(taxpayer=taxpayer, address=address, rental_reg_status=rental_reg_status,
		coc_date=coc_date)

def process_tax_message(row):

	taxpayer = process_taxpayer(row)
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

def process_pre_message(row):

	address = process_address(row['address'])

	if row['corrected_pre'] == "0":
		return "The taxpayer for {address} is not receiving a Principal Residence Exemption, according to the city.".format(address=address)

	elif row['corrected_pre'] == "ADDRESS NOT FOUND":
		return "{address} is not in the city's Principal Residence Exemption data.".format(address=address)

	else:
		return "The taxpayer for {address} is receiving a {PRE}% Principal Residence Exemption, according to the city.".format(address=address, PRE=row['corrected_pre'])

def main(overview_filename, reach_filename):

	#create a reader for the raw overview file
	with open(overview_filename) as fr:
		reader = csv.DictReader(fr)

		#create a writer for the final reach csv
		with open(reach_filename, 'w') as fw:
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
					new_row.append(process_dlba_inventory_message(row))
					new_row.append(process_pre_message(row))

					writer.writerow(new_row)



if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])


