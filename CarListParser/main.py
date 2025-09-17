from classes import CarList
import time


time.sleep(60)
cars_infoid_worker = CarList()
while True:
    cars_infoid_worker.get_infoid_per_page()
