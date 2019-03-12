# Main Housing Data Cleanup

This is the home of Outlier Media data cleaning processes. Most of our data will be processed here. As we grow and take on new types of datasets, our processing may become more specific to the project. 

As with any data journalism project, we must account for entry errors and check the integrity of both our processed data and the data originally provided to us.

## Requirements

* GNU Make
* Python 3
* PostgreSQL
* Google Geocoder API Key
* Requests `pip install requests`


## Run it

Open the Makefile and set the `DATE` variable to today's date in the format `MMDDYYYY`

```
export GOOGLE_MAPS_API_KEY=[your key here]
export DETROIT_PROPERTIES_DB_URL=postgresql://localhost/detroitproperties
export DETROIT_PROPERITES_DB_ROOT_URL=postgresql://localhost
export DETROIT_PROPERITES_DB_NAME=detroitproperties
export DETROIT_PROPERITES_DB_STRING="dbname=detroitproperties"
export CURDIR=[your working directory here]/main-housing-cleanup
export PGDATA=/usr/local/pgsql/data/detroitproperties
```

From the working directory, run `make all` which will: 
* download the most recent data available
* clean it up
* toss it into the postgres database
* join it together
* throw the joined data into a CSV
* configure the CSV with language for Outlier's SMS system
* generate a random sample of 20 rows in a CSV for a quick spot check

## Careful with Google's geocoder

Script requires Google Geocoder API key as an environment variable ( `export GOOGLE_MAPS_API_KEY=[your-key-here] ` ). This is just to correct the invalid zip codes in the Detroit government data (The data portal managers assured us they would be updated. That was in Dec. 2018. Not holding my breath). 

Depending on the size of the dataset, you may need to add a delay to not exceed Google's request limits for a given period. So far, this has not been a problem for us.

