# Citi Bike Data

An app that allows you to see where citi bike trips are taken from/to each month.


### Setup

- You will need a Mapbox API key and it needs to be set as `NEXT_PUBLIC_MAPBOX_API_KEY`
- To get local data, the scripts in the `research` jupyter notbeook file need to be ran. Those scripts will populate data in the `public` directory.

### Current status

- Wrote simple python scripts to extract data from citibike published CSVs and convert to files containing total end-destination trips. 
- Simple frontend setup that prints that data when the user clicks on a marker.
