# Airport Simulator with Air Traffic Control System

Airport is a client-server API using sockets to simulate an air traffic control tower guiding planes for landing. The project includes an airport with specific parameters and requirements for realistic simulation.

## Airport Parameters:

- Cuboid with a square base (side: 10 km, height: 5 km)
- Two airstrips
- Average speed of the plane in the air: 200 m/s
- Landing speed minimum: 110 m/s
- Airstrip length: 3 - 3.5 km
- Airstrip width: 50 m

## Requirements:

- dotenv
- psycopg2
- matplotlib
- numpy
- Standard modules (threading, queue, os, json, time, multiprocessing, random)

## How to Start the Project:

1. **Create Database:**
   - Run `db_creator.py` to create the database. If the database already exists, delete it using `db_delete.py` before creating a new one.

2. **Start the Server:**
   - Run `main_server.py` to start the server.

3. **Start the Client:**
   - Open another terminal and run `main_client.py` to start the client.

## Video Demonstration:

[Watch the application in action on YouTube](https://www.youtube.com/watch?v=rqT0HtlhNb4&feature=youtu.be).

Feel free to contribute or provide feedback!

