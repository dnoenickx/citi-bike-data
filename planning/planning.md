Schema

Trip

- month
- start_station
- end_station

Stations

- Id
- Geometry
- Month (?) – because stations move also can query on station month

API

- Monthly from
  - Takes a list of station IDs
  - Returns a list of station IDs and quantities (the number of trips)

// we want to track scraped docs to ensure we have the latest data. Can compare date modified when scraping to ensure we track changes.
When a doc is new or updated, we can delete all related records and refresh with new data.
Scraped Docs

- Date modified
- File name
- Date
