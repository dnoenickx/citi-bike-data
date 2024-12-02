import requests
from io import BytesIO
import pandas as pd
from zipfile import ZipFile
from h3 import latlng_to_cell

BASE_URL = "https://s3.amazonaws.com/tripdata/"
month = "202410-citibike-tripdata.zip"
latest_data = requests.get(BASE_URL + month)


first_entry_table = pd.DataFrame()
zip_data = BytesIO(latest_data.content)
csv_filename = None

with ZipFile(zip_data) as zip_file:
    for name in zip_file.namelist():
        if name.endswith('.csv'):
            csv_filename = name
            with zip_file.open(name) as csv_file:
                first_entry_table = pd.read_csv(csv_file, dtype={'start_station_id': str, 'end_station_id': str})
                break   



# Get df of station coordinates
start_coords = first_entry_table[['start_station_id', 'start_lat', 'start_lng']].rename(columns={'start_station_id': 'id', 'start_lat': 'lat', 'start_lng': 'lng'})
end_coords = first_entry_table[['end_station_id', 'end_lat', 'end_lng']].rename(columns={'end_station_id': 'id', 'end_lat': 'lat', 'end_lng': 'lng'})
unique_station_coords = pd.concat([start_coords, end_coords]).dropna().drop_duplicates().reset_index(drop=True)


# Calculate H3 Cells
for res in range(10, 16):
    unique_station_coords[f'h3_cell_{res}'] = unique_station_coords.apply(
        lambda row: latlng_to_cell(row['lat'], row['lng'], res), axis=1
    )


# Examine duplicate H3 cells
h3_cell_columns = [col for col in unique_station_coords.columns if col.startswith("h3_cell_")]
for col in h3_cell_columns:
    print(f"\nDuplicate for {col}:")
    unique_station_coords[unique_station_coords[col].duplicated(keep=False)].sort_values(by=col)[['id', 'lat', 'lng', col]]


# Here are the results. Resolution 11 seems like it might be the best choice:

# Duplicate for h3_cell_10:
#                 id        lat        lng       h3_cell_10
# 1875       7940.04  40.821239 -73.917330  8a2a100a9497fff
# 689        7940.02  40.820570 -73.917579  8a2a100a9497fff
# 1611       8205.05  40.839586 -73.900277  8a2a100ad4affff
# 935        8186.01  40.839229 -73.899047  8a2a100ad4affff
# 441        5806.01  40.731690 -73.901590  8a2a100c2957fff
# 529        5764.02  40.731450 -73.900220  8a2a100c2957fff
# 1929       5905.12  40.734548 -73.990761  8a2a100d2297fff
# 1006       5905.12  40.734546 -73.990741  8a2a100d2297fff
# 436        5788.12  40.732233 -73.988900  8a2a100d22d7fff
# 497        5788.16  40.731270 -73.988490  8a2a100d22d7fff
# 14         6190.08  40.743174 -74.003664  8a2a100d249ffff
# 235        6190.03  40.743534 -74.003676  8a2a100d249ffff
# 109        6364.10  40.749640 -73.988050  8a2a100d2c2ffff
# 1005       6364.07  40.749013 -73.988484  8a2a100d2c2ffff
# 1234       6441.02  40.751726 -73.987535  8a2a100d2d0ffff
# 1094       6441.01  40.750977 -73.987654  8a2a100d2d0ffff
# 1220       5779.09  40.729667 -73.980680  8a2a100d3537fff
# 1084       5779.11  40.730311 -73.980472  8a2a100d3537fff
# 1919       6617.02  40.757530 -73.969096  8a2a100d606ffff
# 1109       6617.02  40.757632 -73.969306  8a2a100d606ffff
# 13         3919.07  40.670777 -73.957680  8a2a100db19ffff
# 267        3919.12  40.670529 -73.958222  8a2a100db19ffff
# 1937       4939.07  40.702089 -73.923847  8a2a100dc317fff
# 843        4939.07  40.702013 -73.923769  8a2a100dc317fff
# 1962  Shop Morgan   40.709873 -73.931594  8a2a100dc567fff
# 710         SYS016  40.709628 -73.931457  8a2a100dc567fff
# 835        6115.09  40.742754 -74.007474  8a2a10721ba7fff
# 785        6157.04  40.741982 -74.008316  8a2a10721ba7fff
# 1932       6569.07  40.754610 -73.995295  8a2a10725adffff
# 484        6569.09  40.754145 -73.996089  8a2a10725adffff
# 923        6569.07  40.754623 -73.995168  8a2a10725adffff
# 1254      6569.09_  40.754256 -73.996451  8a2a10725adffff
# 1108       4993.13  40.703367 -74.007868  8a2a10728b8ffff
# 1476       4953.04  40.703554 -74.006702  8a2a10728b8ffff
# 1185       5788.13  40.730207 -73.991026  8a2a1072c90ffff
# 1947       5755.01  40.730257 -73.990417  8a2a1072c90ffff
# 1949       5788.13  40.730250 -73.991081  8a2a1072c90ffff
# 1555       4895.03  40.702461 -73.986842  8a2a1072d0effff
# 511        4895.09  40.701403 -73.986727  8a2a1072d0effff
# 779        4101.17  40.676757 -73.983262  8a2a10774d77fff
# 863        4175.15  40.677274 -73.982820  8a2a10774d77fff

# Duplicate for h3_cell_11:
#             id        lat        lng       h3_cell_11
# 1006   5905.12  40.734546 -73.990741  8b2a100d2294fff
# 1929   5905.12  40.734548 -73.990761  8b2a100d2294fff
# 1109   6617.02  40.757632 -73.969306  8b2a100d6069fff
# 1919   6617.02  40.757530 -73.969096  8b2a100d6069fff
# 843    4939.07  40.702013 -73.923769  8b2a100dc316fff
# 1937   4939.07  40.702089 -73.923847  8b2a100dc316fff
# 484    6569.09  40.754145 -73.996089  8b2a10725adafff
# 1254  6569.09_  40.754256 -73.996451  8b2a10725adafff
# 923    6569.07  40.754623 -73.995168  8b2a10725adcfff
# 1932   6569.07  40.754610 -73.995295  8b2a10725adcfff
# 1185   5788.13  40.730207 -73.991026  8b2a1072c908fff
# 1949   5788.13  40.730250 -73.991081  8b2a1072c908fff

# Duplicate for h3_cell_12:
#            id        lat        lng       h3_cell_12
# 1006  5905.12  40.734546 -73.990741  8c2a100d22947ff
# 1929  5905.12  40.734548 -73.990761  8c2a100d22947ff
# 843   4939.07  40.702013 -73.923769  8c2a100dc3167ff
# 1937  4939.07  40.702089 -73.923847  8c2a100dc3167ff

# Duplicate for h3_cell_13:
#            id        lat        lng       h3_cell_13
# 1006  5905.12  40.734546 -73.990741  8d2a100d229467f
# 1929  5905.12  40.734548 -73.990761  8d2a100d229467f

# Duplicate for h3_cell_14:
# Empty DataFrame
# Columns: [id, lat, lng, h3_cell_14]
# Index: []

# Duplicate for h3_cell_15:
# Empty DataFrame
# Columns: [id, lat, lng, h3_cell_15]
# Index: []
