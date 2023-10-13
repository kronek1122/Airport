import time
import random
from client import PlaneSocket

def flight_number_generator():
        num = 1
        while True:
            yield num
            num += 1

flight_num_gen = flight_number_generator()

while True:
    flight_num = next(flight_num_gen)
    client = PlaneSocket(flight_num)
    client.send_socket()
    time.sleep(1)
