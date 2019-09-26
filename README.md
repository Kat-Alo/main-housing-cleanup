# Main Housing Data Cleanup for Outlier's SMS platform

This is the home of the Outlier Media data cleaning processes for our SMS platform. Here, you can see how our data are wrangled, cleaned up and formatted for our text messages.

The data included on our SMS platform help answer Detroiters' questions about:
* property tax status (e.g. delinquent or subject to foreclosure)
* rental registration
* vacancy, blight and demolition
* whether a property is receiving the Principal Residence Exemption
* a property's auction list status

The majority of our data come from the Detroit Open Data Portal, with a few key exceptions:

### Tax status data

We pay [Loveland Technologies](https://landgrid.com/) for access to tax status data, which they scrape from the Wayne County Treasurer's website.

### Principal Residence Exemption data

Through our reporting, we found that much of the city assessor's Principal Residence Exemption data (presented in the "Parcel Points Ownership" dataset) are inaccurate. Alvin Horhn, a city assessor, sent us an accurate PRE dataset on 8 June 2019. The public data had still not been corrected by 17 July 2019, Horhn said in an email. For the SMS platform, we continue to use the dataset Horhn sent us.

### ZIP codes

As we spotchecked the first few trials of our data processing, we noticed a lot of invalid ZIP codes. After reaching out to the data portal team, a lot of them were corrected, but not all of them. We used Geocodio to geocode all of the addresses. In [`processors/clean-parcel_points_ownership.py`](https://github.com/Kat-Alo/main-housing-cleanup/blob/master/processors/clean-parcel_points_ownership.py) you will see that, if the ZIP code provided in the dataset is not a valid Detroit ZIP code, we pull the ZIP from the Geocodio dataset. 

This does not catch the instances where the ZIP is a valid Detroit ZIP, but is not correct for the given address. (I think this could open a lot of discussion regarding which data sources should be relied on when holding local government agencies accountable. For instance, by erring toward the Assessor's data, we are more likely to have a news consumer catch the error and report back to us. Then we would have a better understanding of data quality issues for the Assessor's Office.)

## Requirements

`pip install -r requirements.txt`

## Run it

```
export DETROIT_PROPERTIES_DB_URL=postgresql://localhost/detroitproperties
export DETROIT_PROPERITES_DB_ROOT_URL=postgresql://localhost
export DETROIT_PROPERITES_DB_NAME=detroitproperties
export DETROIT_PROPERITES_DB_STRING="dbname=detroitproperties"
export CURDIR=[your working directory here]/main-housing-cleanup
export PGDATA=/usr/local/pgsql/data/detroitproperties
```

A shortcut for making the directories to store the data for today:

`make create_directories`

As things are now, we must unfortunately download and migrate the tax status data manually. `make create_directories` should have made a directory `data/raw/[MMDDYYYY]` for today's date. Move the downloaded tax status data to this directory. As long as it is the only file in the directory, the Makefile will identify it as the raw tax status data and process it accordingly.

From the working directory, run `make all` which will: 
* [download the most recent data available](https://github.com/Kat-Alo/main-housing-cleanup/blob/88df56cb633fcac851cc67db13a6cdd9804cb6e4/Makefile#L68)
* [clean it up](https://github.com/Kat-Alo/main-housing-cleanup/blob/88df56cb633fcac851cc67db13a6cdd9804cb6e4/Makefile#L98)
* [toss it into the postgres database](https://github.com/Kat-Alo/main-housing-cleanup/blob/88df56cb633fcac851cc67db13a6cdd9804cb6e4/Makefile#L109)
* [join it together](https://github.com/Kat-Alo/main-housing-cleanup/blob/88df56cb633fcac851cc67db13a6cdd9804cb6e4/Makefile#L122)
* [throw the joined data into a CSV](https://github.com/Kat-Alo/main-housing-cleanup/blob/88df56cb633fcac851cc67db13a6cdd9804cb6e4/Makefile#L125)
* [configure the CSV with language for Outlier's SMS system](https://github.com/Kat-Alo/main-housing-cleanup/blob/88df56cb633fcac851cc67db13a6cdd9804cb6e4/Makefile#L129)
* [generate a random sample of 20 rows in a CSV for a quick spot check](https://github.com/Kat-Alo/main-housing-cleanup/blob/88df56cb633fcac851cc67db13a6cdd9804cb6e4/Makefile#L136)


