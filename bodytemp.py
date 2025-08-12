import random
import time
from sensor import Sensor


class TemperatureSensor(Sensor):
    """
    A class representing a temperature sensor.

    Attributes:
        temp_increase_rate (float): The rate at which the temperature increases.
        T (float): The current temperature.
    """

    def __init__(self, name, start_time, stop_time=None, location=None):
        """
        Initializes the TemperatureSensor.

        Parameters:
            name (str): The name of the sensor.
            start_time (str): The start time for data collection.
            stop_time (str, optional): The stop time for data collection. Defaults to None.
            location (str, optional): The location of the sensor. Defaults to None.
        """
        super().__init__(name, datatype="float", start_time=start_time, stop_time=stop_time, location=location)
        self.temp_increase_rate = 0.05
        self.T = random.uniform(self.min_temp, self.max_temp)

    def start(self):
        """
        Starts the sensor to collect and publish data.
        """
        while self.is_running and self.time >= self.start_time and (
                self.stop_time is None or self.time <= self.stop_time):
            self.publishsensordata(self.getdata())
            time.sleep(1)
            current_datetime = time.localtime()
            self.time = time.strftime("%H:%M:%S", current_datetime)

    def getdata(self):
        """
        Gets the current temperature data.

        Returns:
            float: The current temperature.
        """
        self.T += random.uniform(-self.temp_increase_rate, self.temp_increase_rate)
        return self.T


class AmbientTemperature:
    """
    A class representing the ambient temperature for a location.

    Attributes:
        location (str): The location being monitored.
        time (str): The time of the temperature reading.
        ambient_temperature (float): The ambient temperature.
        upper_threshold (float): The upper threshold for temperature.
        lower_threshold (float): The lower threshold for temperature.
    """

    def __init__(self, location, time, ambient_temperature, upper_threshold, lower_threshold):
        """
        Initializes the AmbientTemperature.

        Parameters:
            location (str): The location being monitored.
            time (str): The time of the temperature reading.
            ambient_temperature (float): The ambient temperature.
            upper_threshold (float): The upper threshold for temperature.
            lower_threshold (float): The lower threshold for temperature.
        """
        self.location = location
        self.time = time
        self.ambient_temperature = ambient_temperature
        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold

    def check_temperature(self):
        """
        Checks if the ambient temperature is within the thresholds.

        Returns:
            str: A message indicating the status of the temperature.
        """
        if self.ambient_temperature > self.upper_threshold:
            return "Temperature is above the upper threshold."
        elif self.ambient_temperature < self.lower_threshold:
            return "Temperature is below the lower threshold."
        else:
            return "Temperature is within the normal range."





import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import numpy as np

def graph_plot_body_temperature():
    try:
        # Load the CSV file with the correct encoding
        df = pd.read_csv('body_temperature.csv', encoding='ISO-8859-1')

        # Capitalize all column names
        df.columns = [col.upper().strip() for col in df.columns]

        # Ensure all required columns are present
        if 'DATE / TIME' not in df.columns or 'LOCATION' not in df.columns or 'TEMPERATURE' not in df.columns or 'TEMPERATURE RANGE' not in df.columns:
            print("Required columns are missing in the CSV file.")
            return

        # Convert 'DATE / TIME' to datetime and sort
        df['DATE / TIME'] = pd.to_datetime(df['DATE / TIME'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        df = df.sort_values('DATE / TIME')

        # Convert 'TEMPERATURE' to numeric, handling any errors
        df['TEMPERATURE'] = pd.to_numeric(df['TEMPERATURE'], errors='coerce')

        # Set up the figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))

        # Customize the grid and ticks
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
        ax.tick_params(axis='x', rotation=45, labelsize=9)
        ax.tick_params(axis='y', labelsize=9)

        # Labels and title
        ax.set_xlabel('Date and Time', fontsize=10, labelpad=10)
        ax.set_ylabel('Temperature (°C)', fontsize=10, labelpad=10)
        ax.set_title('Body Temperature Report by Location', fontsize=12, pad=15)

        # Plot each location with a unique color
        unique_locations = df['LOCATION'].unique()
        colors = plt.cm.tab10(np.linspace(0, 1, len(unique_locations)))
        lines = []

        for location, color in zip(unique_locations, colors):
            location_data = df[df['LOCATION'] == location]
            line, = ax.plot(location_data['DATE / TIME'], location_data['TEMPERATURE'], marker='o',
                            linestyle='-', color=color, linewidth=1.5, markersize=4, label=location)
            lines.append((line, location_data))

        # Define the hover function
        def on_hover(event):
            for line, location_data in lines:
                if event.artist == line:
                    ind = event.target.index
                    location = location_data.iloc[ind]['LOCATION']
                    temperature = location_data.iloc[ind]['TEMPERATURE']
                    current_datetime = location_data.iloc[ind]['DATE / TIME']
                    temp_range = location_data.iloc[ind]['TEMPERATURE RANGE']
                    event.annotation.set_text(
                        f"Date/Time: {current_datetime}\nLocation: {location}\nTemperature: {temperature} °C\nRange: {temp_range}")

        # Enable cursor with hover functionality
        cursor = mplcursors.cursor(hover=True)
        cursor.connect("add", on_hover)

        # Improve layout and legend
        ax.legend(title='Location', fontsize=9, title_fontsize='10', loc='best', fancybox=True, framealpha=0.5)
        plt.tight_layout(pad=1.5)
        plt.show()

    except pd.errors.EmptyDataError:
        print("The CSV file is empty or contains no valid data.")
    except FileNotFoundError:
        print("The CSV file was not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")

import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import numpy as np


def graph_plot_body_temperature2():
    import pandas as pd
    import matplotlib.pyplot as plt
    import mplcursors
    import numpy as np

    try:
        # Load the CSV file
        df = pd.read_csv('body_temperature.csv', encoding='ISO-8859-1')

        # Capitalize all column names
        df.columns = [col.upper().strip() for col in df.columns]

        # Ensure all required columns are present
        required_columns = ['SENSOR ID', 'CALC TEMPERATURE', 'DISTANCE']
        if not all(col in df.columns for col in required_columns):
            print(f"Required columns are missing in the CSV file: {required_columns}")
            return

        # Convert relevant columns to numeric and drop NaN values
        df['CALC TEMPERATURE'] = pd.to_numeric(df['CALC TEMPERATURE'], errors='coerce')
        df['DISTANCE'] = pd.to_numeric(df['DISTANCE'], errors='coerce')
        df = df.dropna(subset=['CALC TEMPERATURE', 'DISTANCE', 'SENSOR ID']).reset_index(drop=True)

        # Ensure there is data to plot
        if df.empty:
            print("The CSV file contains no valid data after cleaning.")
            return

        # Sort the data for better visualization
        df = df.sort_values(by=['DISTANCE', 'CALC TEMPERATURE']).reset_index(drop=True)

        # Set up the figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))

        # Customize the grid and ticks
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
        ax.tick_params(axis='x', labelsize=9)
        ax.tick_params(axis='y', labelsize=9)

        # Labels and title
        ax.set_xlabel('Distance (m)', fontsize=10, labelpad=10)
        ax.set_ylabel('Calculated Temperature (°C)', fontsize=10, labelpad=10)
        ax.set_title('Calculated Temperature vs Distance by Sensor ID', fontsize=12, pad=15)

        # Plot each sensor ID with a unique color
        unique_sensors = df['SENSOR ID'].unique()
        colors = plt.cm.tab10(np.linspace(0, 1, len(unique_sensors)))
        lines = []

        for sensor_id, color in zip(unique_sensors, colors):
            sensor_data = df[df['SENSOR ID'] == sensor_id]
            if not sensor_data.empty:  # Ensure there's data for the sensor
                line, = ax.plot(
                    sensor_data['DISTANCE'].astype(float),
                    sensor_data['CALC TEMPERATURE'].astype(float),
                    marker='o',
                    linestyle='-',
                    color=color,
                    linewidth=1.5,
                    markersize=4,
                    label=sensor_id,
                )
                lines.append((line, sensor_data))

        # Define the hover function
        def on_hover(event):
            for line, sensor_data in lines:
                if event.artist == line:
                    ind = event.target.index
                    sensor_id = sensor_data.iloc[ind]['SENSOR ID']
                    calc_temp = sensor_data.iloc[ind]['CALC TEMPERATURE']
                    distance = sensor_data.iloc[ind]['DISTANCE']
                    event.annotation.set_text(
                        f"Sensor ID: {sensor_id}\n"
                        f"Distance: {distance:.2f} m\n"
                        f"Calculated Temperature: {calc_temp:.2f}°C"
                    )

        # Enable cursor with hover functionality
        cursor = mplcursors.cursor(hover=True)
        cursor.connect("add", on_hover)

        # Improve layout and legend
        ax.legend(title='Sensor ID', fontsize=9, title_fontsize='10', loc='best', fancybox=True, framealpha=0.5)
        plt.tight_layout(pad=1.5)
        plt.show()

    except pd.errors.EmptyDataError:
        print("The CSV file is empty or contains no valid data.")
    except FileNotFoundError:
        print("The CSV file was not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")

