import time
import threading
from client import PlaneSocket

active_threads = 0
def flight_number_generator():
        num = 1
        while True:
            yield num
            num += 1

def create_client(flight_num):
    client = PlaneSocket(flight_num)
    client.send_socket()

flight_num_gen = flight_number_generator()

while True:
    flight_num = next(flight_num_gen)
    print(f"ilość wątków clienta: {active_threads}")
    thread = threading.Thread(target=create_client, args=(flight_num,))
    thread.start()
    active_threads +=1
    time.sleep(5)
