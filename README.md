# Main Housing Data Cleanup

This is the home of Outlier Media data cleaning processes. Most of our data will be processed here. As we grow and take on new types of datasets, our processing may become more specific to the project. 

As with any data journalism project, we must account for entry errors and check the integrity of both our processed data and the data originally provided to us.

## A note about our style conventions

Original and processed data will look similar (although the files _should_ be properly named). To avoid confusion, the headers for original or intermediate data will be all lower case (including acronyms and proper nouns), and final processed data headers WILL-BE-ALL-UPPERCASE-WITH-HYPHENS-INSTEAD-OF-SPACES.

## Careful with Google's geocoder

Script requires Google Geocoder API key as an environment variable ( `export GOOGLE_MAPS_API_KEY=[your-key-here] ` ). Depending on the size of the dataset, you may need to add a delay to not exceed Google's request limits for a given period. So far, this has not been a problem for us.

