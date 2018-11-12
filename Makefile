DATE = 11082018
TABLES = main_housing tax_auction tax_payer
#demolition

.PHONY: all db create_db schema create_tables load_data clean drop_db

all: db create_tables load_data

db: create_db schema
create_tables: $(patsubst %, table_%, $(TABLES))
load_data: $(patsubst %, load_clean_zips_%, $(DATE)) $(patsubst %, load_tax_auction_%, $(DATE)) $(patsubst %, load_tax_payer_%, $(DATE))
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

define check_main_housing_relation
 $(psql) -c "\d public.main_housing" > /dev/null 2>&1
endef

define check_tax_auction_relation
 $(psql) -c "\d public.tax_auction" > /dev/null 2>&1
endef

define check_tax_payer_relation
 $(psql) -c "\d public.tax_payer" > /dev/null 2>&1
endef

########################################################################
#PSQL database administration 
########################################################################

create_db :
	$(check_database) || psql $(DETROIT_PROPERTIES_DB_ROOT_URL) -c "create database $(DETROIT_PROPERITES_DB_NAME) lc_collate \"C\" lc_ctype \"C\" template template0;" && \
	$(psql) -c "CREATE EXTENSION IF NOT EXISTS postgis;"

schema :
	$(psql) -c "CREATE SCHEMA IF NOT EXISTS tmp;"

table_% : data/sql/tables/%.sql
	$(check_public_relation_%) || $(psql) -f $<

drop_db :
	psql $(DETROIT_PROPERTIES_ROOT_URL) -c "drop database $(DETROIT_PROPERITES_DB_NAME);"

########################################################################
#Clean data
########################################################################

.PRECIOUS: data/processed/clean-zips-housing-%.csv
data/processed/clean-zips-housing-%.csv: data/raw-housing-%.csv
	python processors/check-zipcodes.py $< > data/processed/clean-zips-housing-$*.csv 2> data/processed/clean-zips-housing-$*_err.txt

.PRECIOUS: data/proccessed/clean-tax-auction-%.csv
data/processed/clean-tax-auction-%.csv: data/raw-tax-auction-%.csv
	python processors/clean-tax-auction.py $< > data/processed/clean-tax-auction-$*.csv 2> data/processed/clean-tax-auction-$*_err.txt

.PRECIOUS: data/processed/clean-tax-payer-%.csv
data/processed/clean-tax-payer-%.csv: data/raw-tax-payer-%.csv
	python processors/clean-tax-payer.py $< > data/processed/clean-tax-payer-$*.csv 2> data/processed/clean-tax-payer-$*_err.txt

########################################################################
#Load data into PostgreSQL
########################################################################

load_clean_zips_%: data/processed/clean-zips-housing-%.csv
	$(check_main_housing_relation) && $(psql) -c "\copy public.main_housing from '$(CURDIR)/$<' with (delimiter ',', format csv, header);"

load_tax_auction_%: data/processed/clean-tax-auction-%.csv
	$(check_tax_auction_relation) && $(psql) -c "\copy public.tax_auction from '$(CURDIR)/$<' with (delimiter ',', format csv, header);"

load_tax_payer_%: data/processed/clean-tax-payer-%.csv
	$(check_tax_payer_relation) && $(psql) -c "\copy public.tax_payer from '$(CURDIR)/$<' with (delimiter ',', format csv, header);"



########################################################################
#Join and export data as CSV for publication
########################################################################




















