I think it's worth finding a way to just skip using Lyft's station IDs, since they seem difficult to work with across months– especially if this is going to work across cities. This would also make (automated) ingestion very simple, since you only need to access a single month's trip export at a time (an nothing else).

We could simply generate station IDs for unique pairings of lat/long, or better yet make use of Uber's H3 cells as IDs. That strategy would easily deal with stations moving a little bit, or having their ID change within or between months.

I ran a quick analysis on Citi bike data to find H3 resolution that would make sense (research/h3_cell_idea.py).


### Duplicates for h3_cell_10
It's clear the these are too large and grouping multiple stations.

  id |           id  |     lat   |     lng     |  h3_cell_10
-----|---------------|-----------|-------------|------------------
1875 |       7940.04 | 40.821239 | -73.917330  | 8a2a100a9497fff
689  |       7940.02 | 40.820570 | -73.917579  | 
1611 |       8205.05 | 40.839586 | -73.900277  | 8a2a100ad4affff
935  |       8186.01 | 40.839229 | -73.899047  | 
441  |       5806.01 | 40.731690 | -73.901590  | 8a2a100c2957fff
529  |       5764.02 | 40.731450 | -73.900220  | 
1929 |       5905.12 | 40.734548 | -73.990761  | 8a2a100d2297fff
1006 |       5905.12 | 40.734546 | -73.990741  | 
436  |       5788.12 | 40.732233 | -73.988900  | 8a2a100d22d7fff
497  |       5788.16 | 40.731270 | -73.988490  | 
14   |       6190.08 | 40.743174 | -74.003664  | 8a2a100d249ffff
235  |       6190.03 | 40.743534 | -74.003676  | 
109  |       6364.10 | 40.749640 | -73.988050  | 8a2a100d2c2ffff
1005 |       6364.07 | 40.749013 | -73.988484  | 
1234 |       6441.02 | 40.751726 | -73.987535  | 8a2a100d2d0ffff
1094 |       6441.01 | 40.750977 | -73.987654  | 
1220 |       5779.09 | 40.729667 | -73.980680  | 8a2a100d3537fff
1084 |       5779.11 | 40.730311 | -73.980472  | 
1919 |       6617.02 | 40.757530 | -73.969096  | 8a2a100d606ffff
1109 |       6617.02 | 40.757632 | -73.969306  | 
13   |       3919.07 | 40.670777 | -73.957680  | 8a2a100db19ffff
267  |       3919.12 | 40.670529 | -73.958222  | 
1937 |       4939.07 | 40.702089 | -73.923847  | 8a2a100dc317fff
843  |       4939.07 | 40.702013 | -73.923769  | 
1962 |  Shop Morgan  | 40.709873 | -73.931594  | 8a2a100dc567fff
710  |        SYS016 | 40.709628 | -73.931457  | 
835  |       6115.09 | 40.742754 | -74.007474  | 8a2a10721ba7fff
785  |       6157.04 | 40.741982 | -74.008316  | 
1932 |       6569.07 | 40.754610 | -73.995295  | 8a2a10725adffff
484  |       6569.09 | 40.754145 | -73.996089  | 
923  |       6569.07 | 40.754623 | -73.995168  | 
1254 |      6569.09_ | 40.754256 | -73.996451  | 
1108 |       4993.13 | 40.703367 | -74.007868  | 8a2a10728b8ffff
1476 |       4953.04 | 40.703554 | -74.006702  | 
1185 |       5788.13 | 40.730207 | -73.991026  | 8a2a1072c90ffff
1947 |       5755.01 | 40.730257 | -73.990417  | 
1949 |       5788.13 | 40.730250 | -73.991081  | 
1555 |       4895.03 | 40.702461 | -73.986842  | 8a2a1072d0effff
511  |       4895.09 | 40.701403 | -73.986727  | 
779  |       4101.17 | 40.676757 | -73.983262  | 8a2a10774d77fff
863  |       4175.15 | 40.677274 | -73.982820  | 

### Duplicates for h3_cell_11
These on the other hand are grouping stations with consistent IDs
 id  |    id    |    lat    |     lng     |   h3_cell_11
-----|----------|-----------|-------------|-----------------
1006 |  5905.12 | 40.734546 | -73.990741  | 8b2a100d2294fff
1929 |  5905.12 | 40.734548 | -73.990761  | 
1109 |  6617.02 | 40.757632 | -73.969306  | 8b2a100d6069fff
1919 |  6617.02 | 40.757530 | -73.969096  | 
843  |  4939.07 | 40.702013 | -73.923769  | 8b2a100dc316fff
1937 |  4939.07 | 40.702089 | -73.923847  | 
484  |  6569.09 | 40.754145 | -73.996089  | 8b2a10725adafff
1254 | 6569.09_ | 40.754256 | -73.996451  | 
923  |  6569.07 | 40.754623 | -73.995168  | 8b2a10725adcfff
1932 |  6569.07 | 40.754610 | -73.995295  | 
1185 |  5788.13 | 40.730207 | -73.991026  | 8b2a1072c908fff
1949 |  5788.13 | 40.730250 | -73.991081  | 

### Duplicates for h3_cell_12
And these are missing results from h3_cell_11 that are the same ID
 id  |    id   |   lat     |    lng      |    h3_cell_12
-----|---------|-----------|-------------|-----------------
1006 | 5905.12 | 40.734546 | -73.990741  | 8c2a100d22947ff
1929 | 5905.12 | 40.734548 | -73.990761  | 
843  | 4939.07 | 40.702013 | -73.923769  | 8c2a100dc3167ff
1937 | 4939.07 | 40.702089 | -73.923847  | 

### Duplicates for h3_cell_13
 id  |       id |       lat |      lng    |   h3_cell_13
-----|----------|-----------|-------------|-----------------
1006 |  5905.12 | 40.734546 | -73.990741  | 8d2a100d229467f
1929 |  5905.12 | 40.734548 | -73.990761  | 8d2a100d229467f


Cell sizes slowly vary across latitudes, so the setting may have to be different for different cities. Examining one of our resoltion 11 cells in NYC, it is 2160 m2.

You can view the cell here: https://h3geo.org/#hex=8b2a100d2294fff


## Idea for basic JSON scheme:

```json
{
  stations: {
    "8b2a100d2294fff": {
      "name": "Broadway & E 14 St",
      "id": "8b2a100d2294fff",
      "latitude": 40.734546,
      "longitude": -73.990741
    },
    "8b2a100d6069fff": {
      "name": "E 53 St & 3 Ave",
      "id": "8b2a100d6069fff",
      "latitude": 40.757632,
      "longitude": -73.969306
    }
  },
  origin_trips : {
    "8b2a100d2294fff": {
      "8b2a100d2294fff": 56,
      "8b2a100d6069fff": 10
    },
    "8b2a100d6069fff": {
      "8b2a100d2294fff": 23,
      "8b2a100d6069fff": 50
    }
  },
  destination_trips : {
    "8b2a100d2294fff": {
      "8b2a100d2294fff": 56,
      "8b2a100d6069fff": 65
    },
    "8b2a100d6069fff": {
      "8b2a100d2294fff": 18,
      "8b2a100d6069fff": 64
    }
  }
}
```