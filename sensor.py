import time
from queue import Queue
from typing import Optional

# Define a list of indoor locations
indoor_locations = ["Living Room", "Kitchen", "Toilet", "Bathroom", "Bedroom", "Staircase", "Passage", "Office"]
positions = ["Sitting", "Standing", "Lying down", "Lying on couch"]
moving_pattern = ["Random", "Fast", "Normal"]


class Sensor:
    def __init__(self, name, datatype, start_time, stop_time=None, location=None):
        self.name = name
        self.datatype = datatype
        self.start_time = start_time
        self.stop_time = stop_time
        self.location = location
        self.is_running = False

    def start(self):
        self.is_running = True
        self.time = time.strftime("%H:%M:%S")

    def stop(self):
        self.is_running = False

    def getdata(self):
        raise NotImplementedError("The getdata method must be implemented by subclasses.")