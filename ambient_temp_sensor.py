# temp_sensor.py

class TemperatureSensor:
    def __init__(self, name, start_time, stop_time, location=None, temperature_data=None):
        self.name = name
        self.start_time = start_time
        self.stop_time = stop_time
        self.location = location
        self.temperature_data = temperature_data
        self.current_temp_index = 0

        # if self.temperature_data is not None:
        #     print(f"Temperature data initialized for {self.name}.")
        # else:
        #     print(f"Temperature data is None for {self.name}.")

    def update_temperature(self):
        # Ensure the temperature data is loaded
        if self.temperature_data is not None:
            if self.current_temp_index < len(self.temperature_data):
                self.current_temp = self.temperature_data.iloc[self.current_temp_index]['TEMPERATURE']
                self.current_temp_index += 1
            else:
                # Loop over the data if it runs out
                self.current_temp_index = 0
                self.current_temp = self.temperature_data.iloc[self.current_temp_index]['TEMPERATURE']
        else:
            raise ValueError("Temperature data is not loaded properly.")

    def getdata(self):
        self.update_temperature()
        return self.current_temp


import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
from itertools import cycle
import numpy as np


def graph_plot():
    try:
        # Load the CSV file with the correct encoding
        df = pd.read_csv('ambient_temperature.csv', encoding='ISO-8859-1')

        # Print out the column names to debug
        # print("Columns in the CSV file:", df.columns)

        # Capitalize all column names
        df.columns = [col.upper().strip() for col in df.columns]

        # Map the columns to the correct names
        if 'DATE / TIME' not in df.columns or 'LOCATION' not in df.columns or 'AMBIENT TEMPERATURE' not in df.columns:
            print("Required columns are missing in the CSV file.")
            return
        try:
            df['DATE / TIME'] = pd.to_datetime(df['DATE / TIME'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        except ValueError:
            print("Date parsing failed. Check the date format in your CSV file.")
            return

        # Convert 'DATE / TIME' to datetime and sort
        df['DATE / TIME'] = pd.to_datetime(df['DATE / TIME'])
        df = df.sort_values('DATE / TIME')

        # Convert 'TEMPERATURE' to numeric, handling any errors
        df['AMBIENT TEMPERATURE'] = pd.to_numeric(df['AMBIENT TEMPERATURE'], errors='coerce')

        # Set up the figure and axis with a smaller size
        fig, ax = plt.subplots(figsize=(10, 6))  # Adjusted figure size for a more optimal look

        # Customize the grid and ticks
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
        ax.tick_params(axis='x', rotation=45, labelsize=9)  # Smaller font size for x-axis labels
        ax.tick_params(axis='y', labelsize=9)  # Smaller font size for y-axis labels

        # Labels and title
        ax.set_xlabel('Date and Time', fontsize=10, labelpad=10)
        ax.set_ylabel('Ambient Temperature (°C)', fontsize=10, labelpad=10)
        ax.set_title('Ambient Temperature Report by Location', fontsize=12, pad=15)

        # Customize the color cycle
        unique_locations = df['LOCATION'].unique()
        colors = plt.cm.tab10(np.linspace(0, 1, len(unique_locations)))

        lines = []
        color_cycle = cycle(colors)
        for location in unique_locations:
            location_data = df[df['LOCATION'] == location]
            color = next(color_cycle)
            line, = ax.plot(location_data['DATE / TIME'], location_data['AMBIENT TEMPERATURE'], marker='o',
                            linestyle='-', color=color, linewidth=1.5, markersize=4, label=location)
            lines.append((line, location_data))

        # Define the hover function
        def on_hover(event):
            for line, location_data in lines:
                if event.artist == line:
                    ind = event.target.index
                    location = location_data.iloc[ind]['LOCATION']
                    temperature = location_data.iloc[ind]['AMBIENT TEMPERATURE']
                    current_datetime = location_data.iloc[ind]['DATE / TIME']
                    temp_range = location_data.iloc[ind]['TEMPERATURE RANGE']
                    event.annotation.set_text(
                        f"{current_datetime}\nLocation: {location}\nTemperature: {temperature}\nRange: {temp_range}")

        # Enable cursor with hover functionality
        cursor = mplcursors.cursor(hover=True)
        cursor.connect("add", on_hover)

        # Improve layout and legend
        ax.legend(title='Location', fontsize=9, title_fontsize='10', loc='best', fancybox=True, framealpha=0.5)
        plt.tight_layout(pad=1.5)  # Adjust padding to fit everything neatly
        plt.show()

    except pd.errors.EmptyDataError:
        print("The CSV file is empty or contains no valid data.")
    except FileNotFoundError:
        print("The CSV file was not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")