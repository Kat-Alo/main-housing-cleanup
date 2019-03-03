DATE = 02222019
TAX_DATE = 02112019
DIRECTORIES = raw processed
DOWNLOADS = parcel_points_ownership blight_violations rental_registrations upcoming_demolitions demolition_pipeline vacant_certifications vacant_registrations dlba_inventory dlba_properties_sale
TABLES = parcel_points_ownership blight_violations rental_registrations tax_auction upcoming_demolitions demolition_pipeline vacant_certifications vacant_registrations dlba_inventory dlba_properties_sale
VIEWS = blight_count data_overview

.PHONY: all create_directories download db create_db schema create_tables load_data create_views clean drop_db

all: db create_tables load_data create_views data/processed/$(DATE)/reach_webhook.csv

create_directories: $(patsubst %, directory_%, $(DIRECTORIES))
download: $(patsubst %, data/raw/$(DATE)/raw-%.csv, $(DOWNLOADS))
process_data: $(patsubst %, data/processed/$(DATE)/clean-%.csv, $(TABLES))
db: create_db schema
create_tables: $(patsubst %, table_%, $(TABLES))
load_data: $(patsubst %, load_%, $(TABLES))
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
#PSQL database administration $(psql) && \ -c "CREATE EXTENSION IF NOT EXISTS postgis;"
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
	curl "https://data.detroitmi.gov/api/views/dxgi-9s8s/rows.csv?accessType=DOWNLOAD" > $@

data/raw/$(DATE)/raw-rental_registrations.csv:
	curl "https://data.detroitmi.gov/api/views/64cb-n6dd/rows.csv?accessType=DOWNLOAD" > $@

data/raw/$(DATE)/raw-blight_violations.csv:
	curl "https://data.detroitmi.gov/api/views/ti6p-wcg4/rows.csv?accessType=DOWNLOAD" > $@

data/raw/$(DATE)/raw-upcoming_demolitions.csv:
	curl "https://data.detroitmi.gov/api/views/tsqq-qtet/rows.csv?accessType=DOWNLOAD" > $@

data/raw/$(DATE)/raw-demolition_pipeline.csv:
	curl "https://data.detroitmi.gov/api/views/urqn-dpd3/rows.csv?accessType=DOWNLOAD&bom=true&query=select+*" > $@

data/raw/$(DATE)/raw-vacant_certifications.csv:
	curl "https://data.detroitmi.gov/api/views/8vfc-77i7/rows.csv?accessType=DOWNLOAD" > $@

data/raw/$(DATE)/raw-vacant_registrations.csv:
	curl "https://data.detroitmi.gov/api/views/futm-xtvg/rows.csv?accessType=DOWNLOAD" > $@

data/raw/$(DATE)/raw-dlba_inventory.csv:
	curl "https://data.detroitmi.gov/api/views/vsin-ur7i/rows.csv?accessType=DOWNLOAD" > $@

data/raw/$(DATE)/raw-dlba_properties_sale.csv:
	curl "https://data.detroitmi.gov/api/views/gfhb-f4i5/rows.csv?accessType=DOWNLOAD" > $@

data/raw/$(DATE)/raw-tax_auction.csv:
	python processors/get-raw-tax-data.py data/raw/$(DATE)/raw-tax_auction.csv > data/raw/$(DATE)/raw-tax_auction.csv

########################################################################
#Clean data
########################################################################

.PRECIOUS: data/processed/$(DATE)/clean-%.csv
data/processed/$(DATE)/clean-%.csv: data/raw/$(DATE)/raw-%.csv
	python processors/clean-$*.py $< $@ > data/processed/$(DATE)/clean-$*.csv 2> data/processed/$(DATE)/clean-$*_err.txt

########################################################################
#Load data into PostgreSQL
########################################################################

load_%: data/processed/$(DATE)/clean-%.csv
	$(psql) -c "\copy public.$* from '$(CURDIR)/$<' with (delimiter ',', format csv, header);"

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


