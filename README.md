# Airport

Client-Server API, use sockets. The airport simulator.

The air traffic control tower (server) automatically brings planes (clients) to land. 
A maximum of 100 planes can be in the air (db_connection_pool takes care of that)

Airport parameters:
    - a cuboid with a square base, side 10 km and height 5 km
    - two airstrips
    - average speed of the plane in the air: 250 m/s
    - landing speed min: 80 m/s
    - airstrip length 3 - 3.5 km
    - airstrip width 50m

Requirements: 
- dotenv
- psycopg2
- matplotlib
- numpy
- standards modules (threading, queue, os, time, multiprocessing)


