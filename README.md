# Airport

Client-Server API, use sockets. The airport simulator.

The air traffic control tower (server) automatically brings planes (clients) to land. 

A maximum of 100 planes can be in the air (db_connection_pool takes care of that)

Airport parameters:
- a cuboid with a square base, side 10 km and height 5 km
- two airstrips
- average speed of the plane in the air: 200 m/s
- landing speed min: 110 m/s
- airstrip length 3 - 3.5 km
- airstrip width 50m

Requirements: 
- dotenv
- psycopg2
- matplotlib
- numpy
- standards modules (threading, queue, os, json, time, multiprocessing, random)

How to start project:
1. Create database, run db_creator.py (if database exist, first delete existing db - use db_delete.py file)
2. Start the server, run the main_server.py file
3. Start the client from another terminal, run main_client.py file

Link to a video of the application in action: https://www.youtube.com/watch?v=rqT0HtlhNb4&feature=youtu.be


