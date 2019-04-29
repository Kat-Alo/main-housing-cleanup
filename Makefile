DATE = $(shell date +'%m%d%Y')
SPOTCHECK_SAMPLE_SIZE = 20
TAX_RAW_FILENAME = 20190405-5ca7ec476aab9e78766a64a2.csv
TAX_PROCESSED_FILENAME = tax_data_04082019.csv

#searches for the most recent Loveland scrape of the Treasurer's data, returns date of scrape
# tax_status_date = $(shell python processors/get-raw-tax-data.py data/raw/$(DATE))

#helpful to test
# echo:
# 	echo $(tax_status_date)

DIRECTORIES = processed raw
DOWNLOADS = parcel_points_ownership blight_violations rental_registrations upcoming_demolitions demolition_pipeline vacant_certifications vacant_registrations dlba_inventory dlba_properties_sale
TABLES = parcel_points_ownership blight_violations rental_registrations tax_status upcoming_demolitions demolition_pipeline vacant_certifications vacant_registrations dlba_inventory dlba_properties_sale
LOAD = parcel_points_ownership blight_violations rental_registrations upcoming_demolitions demolition_pipeline vacant_certifications vacant_registrations dlba_inventory dlba_properties_sale
VIEWS = blight_count data_overview

.PHONY: all create_directories tax_status_date download db create_db schema create_tables clean_tax_data load_tax_data load_data create_views clean drop_db

all: db create_tables clean_tax_data load_data create_views data/processed/$(DATE)/reach_spotcheck.csv

create_directories: $(patsubst %, directory_%, $(DIRECTORIES))
download: $(patsubst %, data/raw/$(DATE)/raw-%.csv, $(DOWNLOADS))
process_data: $(patsubst %, data/processed/$(DATE)/clean-%.csv, $(TABLES))
db: create_db schema
create_tables: $(patsubst %, table_%, $(TABLES))
load_data: load_tax_data load_portal_data
load_portal_data: $(patsubst %, data_portal_load_%, $(LOAD)) 
create_views: $(patsubst %, view_%, $(VIEWS))
clean: drop_db


########################################################################
#PSQL Database check functions
########################################################################

define psql
	psql $(DETROIT_PROPERTIES_DB_URL)
endef

define check_database
 $(psql) -c "select 1;" > /dev/null 2>&1
endef

define check_public_relation_%
 $(psql) -c "\d public.%" > /dev/null 2>&1
endef

########################################################################
#PSQL database administration
########################################################################

create_db :
	$(check_database) || psql $(DETROIT_PROPERTIES_DB_ROOT_URL) -c "create database $(DETROIT_PROPERITES_DB_NAME) lc_collate \"C\" lc_ctype \"C\" template template0;"

schema :
	$(psql) -c "CREATE SCHEMA IF NOT EXISTS tmp;"

table_% : data/sql/tables/%.sql
	$(check_public_relation_%) || $(psql) -f $<

drop_db :
	psql $(DETROIT_PROPERTIES_ROOT_URL) -c "drop database $(DETROIT_PROPERITES_DB_NAME);"

########################################################################
#Create new directories for today's data download
########################################################################

directory_%:
	mkdir data/$*/$(DATE)

########################################################################
#Download data
########################################################################
data/raw/$(DATE)/raw-parcel_points_ownership.csv:
	curl -o $@ "https://data.detroitmi.gov/api/views/dxgi-9s8s/rows.csv?accessType=DOWNLOAD"

data/raw/$(DATE)/raw-rental_registrations.csv:
	curl -o $@ "https://data.detroitmi.gov/api/views/64cb-n6dd/rows.csv?accessType=DOWNLOAD"

data/raw/$(DATE)/raw-blight_violations.csv:
	curl -o $@ "https://data.detroitmi.gov/api/views/ti6p-wcg4/rows.csv?accessType=DOWNLOAD"

data/raw/$(DATE)/raw-upcoming_demolitions.csv:
	curl -o $@ "https://data.detroitmi.gov/api/views/tsqq-qtet/rows.csv?accessType=DOWNLOAD"

data/raw/$(DATE)/raw-demolition_pipeline.csv:
	curl -o $@ "https://data.detroitmi.gov/api/views/urqn-dpd3/rows.csv?accessType=DOWNLOAD&bom=true&query=select+*"

data/raw/$(DATE)/raw-vacant_certifications.csv:
	curl -o $@ "https://data.detroitmi.gov/api/views/8vfc-77i7/rows.csv?accessType=DOWNLOAD"

data/raw/$(DATE)/raw-vacant_registrations.csv:
	curl -o $@ "https://data.detroitmi.gov/api/views/futm-xtvg/rows.csv?accessType=DOWNLOAD"

data/raw/$(DATE)/raw-dlba_inventory.csv:
	curl -o $@ "https://data.detroitmi.gov/api/views/vsin-ur7i/rows.csv?accessType=DOWNLOAD"

data/raw/$(DATE)/raw-dlba_properties_sale.csv:
	curl -o $@ "https://data.detroitmi.gov/api/views/gfhb-f4i5/rows.csv?accessType=DOWNLOAD"

########################################################################
#Clean data
########################################################################

.PRECIOUS: data/processed/$(DATE)/clean-%.csv
data/processed/$(DATE)/clean-%.csv: data/raw/$(DATE)/raw-%.csv
	python processors/clean-$*.py $< $@ > data/processed/$(DATE)/clean-$*.csv 2> data/processed/$(DATE)/clean-$*_err.txt

# .PRECIOUS: data/processed/$(DATE)/clean-%_tax_status.csv
# data/processed/$(DATE)/clean-%_tax_status.csv: data/raw/$(DATE)/$(tax_status_date).csv
# 	python processors/clean-tax_status.py $< $@ > data/processed/$(DATE)/clean-$(tax_status_date)_tax_status.csv 2> data/processed/$(DATE)/clean-$(tax_status_date)_tax_status_err.txt
# > data/processed/$(DATE)/clean-$(tax_status_date)_tax_status.csv 2> data/processed/$(DATE)/clean-$(tax_status_date)_tax_status_err.txt
clean_tax_data:
	python processors/clean-tax_status.py "data/raw/$(DATE)/$(TAX_RAW_FILENAME)" "data/processed/$(DATE)/$(TAX_PROCESSED_FILENAME)"

########################################################################
#Load data into PostgreSQL
########################################################################

data_portal_load_%: data/processed/$(DATE)/clean-%.csv
	$(psql) -c "\copy public.$* from '$(CURDIR)/$<' with (delimiter ',', format csv, header);"

load_tax_data:
	$(psql) -c "\copy public.tax_status from '$(CURDIR)/data/processed/$(DATE)/$(TAX_PROCESSED_FILENAME)' with (delimiter ',', format csv, header);"

########################################################################
#Join and export data as CSV for internal use
########################################################################

view_%: data/sql/views/%.sql
	$(psql) -f $<

data/processed/$(DATE)/data_overview.csv:
	$(psql) -c "\copy (SELECT * FROM data_overview) TO '$(CURDIR)/$@' with (delimiter ',', format csv, header);"

########################################################################
#Process overview CSV with text for GroundSource
########################################################################

data/processed/$(DATE)/groundsource_webhook.csv: data/processed/$(DATE)/data_overview.csv
	python processors/groundsource_webhook.py $< $@ > data/processed/$(DATE)/groundsource_webhook.csv 2> data/processed/$(DATE)/groundsource_webhook_err.txt

########################################################################
#Process overview CSV with text for Reach
########################################################################

data/processed/$(DATE)/reach_webhook.csv: data/processed/$(DATE)/data_overview.csv
	python processors/reach_webhook.py $< $@ > data/processed/$(DATE)/reach_webhook.csv 2> data/processed/$(DATE)/reach_webhook_err.txt

########################################################################
#Generate spotcheck file from reach_webhook
########################################################################

data/processed/$(DATE)/reach_spotcheck.csv: data/processed/$(DATE)/reach_webhook.csv
	python processors/spotcheck-generator.py $< $@ $(SPOTCHECK_SAMPLE_SIZE) > data/processed/$(DATE)/reach_spotcheck.csv 2> data/processed/$(DATE)/reach_spotcheck_err.txt










