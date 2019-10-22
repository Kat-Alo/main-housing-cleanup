DATE = $(shell date +'%m%d%Y')
TAX_RAW_FILENAME = $(shell python processors/get_tax_raw_filename.py)
TAX_PROCESSED_FILENAME = $(shell python processors/get_tax_processed_filename.py $(TAX_RAW_FILENAME))

SPOTCHECK_SAMPLE_SIZE = 20

DIRECTORIES = processed raw
DOWNLOADS = parcels blight_violations rental_registrations_historic demolitions_under_contract demolition_pipeline vacant_certifications dlba_inventory dlba_properties_sale
TABLES = parcels blight_violations rental_registrations_historic tax_status demolitions_under_contract demolition_pipeline vacant_certifications dlba_inventory dlba_properties_sale
LOAD = parcels blight_violations rental_registrations_historic demolitions_under_contract demolition_pipeline vacant_certifications dlba_inventory dlba_properties_sale
VIEWS = blight_count data_overview

#Datasets that are unavailable on Detroit's open data portal as of 10/21/2019:
	#vacant_registrations

.PHONY: all directories tax_status_date download db create_db schema create_tables clean_tax_data load_tax_data load_data create_views clean drop_db

all: db create_tables clean_tax_data load_data create_views data/processed/$(DATE)/reach_spotcheck.csv

directories: $(patsubst %, directory_%, $(DIRECTORIES))
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
	$(check_database) || psql $(DETROIT_PROPERTIES_DB_ROOT_URL) -c "create database $(DETROIT_PROPERTIES_DB_NAME) lc_collate \"C\" lc_ctype \"C\" template template0;"

schema :
	$(psql) -c "CREATE SCHEMA IF NOT EXISTS tmp;"

table_% : data/sql/tables/%.sql
	$(check_public_relation_%) || $(psql) -f $<

drop_db :
	psql $(DETROIT_PROPERTIES_ROOT_URL) -c "drop database $(DETROIT_PROPERTIES_DB_NAME);"

########################################################################
#Create new directories for today's data download
########################################################################

directory_%:
	mkdir data/$*/$(DATE)

########################################################################
#Download data
########################################################################
data/raw/$(DATE)/raw-parcels.csv:
	curl -o $@ "https://opendata.arcgis.com/datasets/a79a16f9fa5d4c0c84957cb96d7250ce_0.csv"

data/raw/$(DATE)/raw-rental_registrations_historic.csv:
	curl -o $@ "https://opendata.arcgis.com/datasets/d563b1e6fa1e4740bd5bc78ff75a94ea_0.csv"

data/raw/$(DATE)/raw-rental_registrations_current.csv:
	curl -o $@ "https://opendata.arcgis.com/datasets/4bf945db092b4adaa0949fda2fc6a0af_0.csv"

data/raw/$(DATE)/raw-rental_certifications_historic.csv:
	curl -o $@ "https://opendata.arcgis.com/datasets/f387316a090e45b397a173baef5eb131_0.csv"

data/raw/$(DATE)/raw-rental_inspections_historic.csv:
	curl -o $@ "https://opendata.arcgis.com/datasets/97664edd5ead444282e348e566de4eea_0.csv"

data/raw/$(DATE)/raw-blight_violations.csv:
	curl -o $@ "https://opendata.arcgis.com/datasets/5854b96be15b44f2a7ee85f2702790e7_0.csv"

data/raw/$(DATE)/raw-demolitions_under_contract.csv:
	curl -o $@ "https://opendata.arcgis.com/datasets/e506c103f3a045a1aa53f7cd8e70dc1d_0.csv"

data/raw/$(DATE)/raw-demolition_pipeline.csv:
	curl -o $@ "https://opendata.arcgis.com/datasets/0d81898958304265ac45d2f59a7339f5_0.csv"

data/raw/$(DATE)/raw-vacant_certifications.csv:
	curl -o $@ "https://opendata.arcgis.com/datasets/755864d640094e2a985f5b0d45e9bc24_0.csv"

data/raw/$(DATE)/raw-vacant_registrations.csv:
	curl -o $@ "https://opendata.arcgis.com/datasets/8d0c2d45644442ac990bffc2cb3a55b9_0.csv"

data/raw/$(DATE)/raw-dlba_inventory.csv:
	curl -o $@ "https://opendata.arcgis.com/datasets/04ba7b817d1d45ba89aab539af7ec438_0.csv"

data/raw/$(DATE)/raw-dlba_properties_sale.csv:
	curl -o $@ "https://opendata.arcgis.com/datasets/dfb563f061b74f60b799c5eeae617fc8_0.csv"

########################################################################
#Clean data
########################################################################

.PRECIOUS: data/processed/$(DATE)/clean-%.csv
data/processed/$(DATE)/clean-%.csv: data/raw/$(DATE)/raw-%.csv
	python processors/clean-$*.py $< $@ > data/processed/$(DATE)/clean-$*.csv 2> data/processed/$(DATE)/clean-$*_err.txt

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
#Process overview CSV with text for Reach
########################################################################

data/processed/$(DATE)/reach_webhook.csv: data/processed/$(DATE)/data_overview.csv
	python processors/reach_webhook.py $< $@ > data/processed/$(DATE)/reach_webhook.csv 2> data/processed/$(DATE)/reach_webhook_err.txt

########################################################################
#Generate spotcheck file from reach_webhook
########################################################################

data/processed/$(DATE)/reach_spotcheck.csv: data/processed/$(DATE)/reach_webhook.csv
	python processors/spotcheck-generator.py $< $@ $(SPOTCHECK_SAMPLE_SIZE) > data/processed/$(DATE)/reach_spotcheck.csv 2> data/processed/$(DATE)/reach_spotcheck_err.txt










