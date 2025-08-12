import csv
import time

class Diary:
    def __init__(self, log_sensor_data=None, log_process=None, log_action=None, time_interval=None, publisher=None,
                 subscribers=None):
        self.log_sensor_data = log_sensor_data or [""]
        self.log_process = log_process or []
        self.log_action = log_action or []
        self.time_interval = time_interval or 0
        self.publisher = publisher or ""
        self.subscribers = subscribers or []

    log_sensor_data = [""]
    temp_range = ""
    temp_range2 = ""
    co2_range = [""]

def log_process(file_name, column_titles, data):
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([])  # Add a blank row if needed
        writer.writerow(column_titles)
        writer.writerows(data)

def log_body_temperature():
    log_process(
        'body_temperature.csv',
        'DATE / TIME, LOCATION, TEMPERATURE, CALC TEMPERATURE, DISTANCE, TEMPERATURE RANGE, SENSOR ID'.split(", "),
        Diary.log_sensor_data
    )

def log_motion_sensor():
    log_process(
        'motion_sensor_log.csv',
        'DATE / TIME, LOCATION, MOVEMENT PATTERN, BODY POSITION, HEALTH STATUS'.split(", "),
        Diary.log_sensor_data
    )

def log_ambient_temperature():
    log_process(
        'ambient_temperature.csv',
        'DATE / TIME, LOCATION, AMBIENT TEMPERATURE, TEMPERATURE RANGE'.split(", "),
        Diary.log_sensor_data
    )

def log_co2_emission():
    log_process(
        'CO2_Emission.csv',
        'SENSOR_ID, DATE / TIME, C02 EMISSION (ppm), CHANGE IN %, ACTIONS_TAKEN'.split(", "),
        Diary.co2_range
    )
