import random
import time
import pandas as pd
from sensor import Sensor


class TemperatureSensor:
    def __init__(self, name, start_time, stop_time=None, location=None, temperature_data=None, date=None):
        self.name = name
        self.datatype = "float"
        self.start_time = start_time
        self.stop_time = stop_time
        self.location = location
        self.temperature_data = temperature_data  # DataFrame with 'TEMPERATURE' column
        self.current_temp_index = 0  # Start at the beginning of the temperature data
        self.current_temp = None  # Placeholder for the current temperature
        self.is_running = False
        self.date = date


    def start(self):
        self.is_running = True
        self.time = time.strftime("%H:%M:%S")

    def getdata(self):
        # Update the temperature before returning it
        self.update_temperature()
        return self.current_temp

    def stop(self):
        self.is_running = False

    def update_temperature(self):
        # Check if there is more temperature data to read
        if self.current_temp_index < len(self.temperature_data):
            # Access the temperature value from the current row
            self.current_temp = self.temperature_data.iloc[self.current_temp_index]['TEMPERATURE']
            self.current_temp_index += 1  # Move to the next row
        else:
            # If all data has been read, reset to the beginning or stop
            self.current_temp_index = 0
            self.current_temp = self.temperature_data.iloc[self.current_temp_index]['TEMPERATURE']

