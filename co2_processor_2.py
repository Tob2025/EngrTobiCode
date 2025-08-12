import random
import time
import csv
import pandas as pd
import communication_action
import windows_action
import door_action
import robot_action
import diary
from co2_sensor import CO2Monitoring


class CO2Processor(CO2Monitoring):
    @staticmethod
    def process_conditions():
        change_in_percentage = []

        try:
            with open('co2_csv_file.csv', 'r') as file:
                reader = csv.reader(file)
                co2_emission_data = list(reader)

            row_count = len(co2_emission_data)
            count = 1  # Start from the first data row (skip the header)

            file_path = 'co2_csv_file.csv'
            column_name = 'co2'
            moving_average = CO2Processor.calculate_moving_average(file_path, column_name)
            count_moving_average = 0

            while count < row_count:
                if len(co2_emission_data[count]) < 3:
                    print(f"Skipping row {count} due to insufficient columns: {co2_emission_data[count]}")
                    count += 1
                    continue

                try:
                    sensor_id = co2_emission_data[count][0]
                    current_datetime = co2_emission_data[count][1]
                    co2_emission = int(co2_emission_data[count][2])

                    if count > 1:  # Calculate change in percentage starting from the second data row
                        previous_emission = int(co2_emission_data[count - 1][2])
                        change = ((
                                              co2_emission - previous_emission) / previous_emission) * 100 if previous_emission != 0 else 0
                        change_in_percentage.append(change)
                    else:
                        change = 0  # No change for the first data point

                except (IndexError, ValueError) as e:
                    print(f"Error at row {count}: {e}")
                    change = None

                if change is not None:
                    CO2Processor.handle_co2_levels(sensor_id, current_datetime, co2_emission, change,
                                                   moving_average[count_moving_average])

                count_moving_average += 1
                count += 1

        except FileNotFoundError:
            print("The CSV file was not found. Please check the file path.")
        except Exception as e:
            print(f"An error occurred while processing the file: {e}")

        return change_in_percentage

    @staticmethod
    def calculate_moving_average(file_path, column_name):
        df = pd.read_csv(file_path)
        if column_name not in df.columns:
            return []
        values = df[column_name]
        moving_averages = []
        for i in range(len(values)):
            if i < 5:
                average = values[:i + 1].mean()
            else:
                average = values[i - 5:i + 1].mean()
            moving_averages.append(average)
        return moving_averages

    @staticmethod
    def handle_co2_levels(sensor_id, current_datetime, co2_emission, change, moving_average):
        if co2_emission < (moving_average * 2):
            data = [sensor_id, current_datetime, co2_emission, f"{change:.2f}%", "No Action. Normal Health"]
            diary.Diary.co2_range.append(data)
            print(f"""
                CO2 emitted at {current_datetime} is {co2_emission}ppm, which is NORMAL
                Sensor ID = {sensor_id}
                Change in Percentage = {change:.2f}%
            """)
            time.sleep(2)
        elif co2_emission > (moving_average * 2.5):
            data = [sensor_id, current_datetime, co2_emission, f"{change:.2f}%",
                    "Reduce number of occupants. All vent fans ON. All doors opened. All windows opened"]
            diary.Diary.co2_range.append(data)
            print(f"""
                CO2 emitted at {current_datetime} is {co2_emission}ppm, which is ABNORMAL
                Sensor ID = {sensor_id}
                Incident Time = {current_datetime}
                Change in Percentage = {change:.2f}%
            """)
            print("Ventilation fan ON")
            robot_action.activate_robot_co2_check()
            time.sleep(2)
            door_action.adjustDoor()
            time.sleep(2)
            windows_action.adjust_window()
            time.sleep(2)
        elif co2_emission > (moving_average * 2):
            data = [sensor_id, current_datetime, co2_emission, f"{change:.2f}%",
                    "Vent fan ON. Door opened. Window opened."]
            diary.Diary.co2_range.append(data)
            print(f"""
                CO2 emitted at {current_datetime} is {co2_emission}ppm, which is ABNORMAL
                Sensor ID = {sensor_id}
                Incident Time = {current_datetime}
                Change in Percentage = {change:.2f}%
                The emission rate has doubled. Reduce number of people in location.
            """)
            print("Ventilation fan ON")
            time.sleep(2)
            door_action.adjustDoor()
            time.sleep(2)
            windows_action.adjust_window()
            time.sleep(2)




import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
from itertools import cycle
import numpy as np

def graph_plot():
    try:
        df = pd.read_csv('co2_csv_file.csv')

        if df.empty:
            print("The CSV file is empty.")
            return

        if 'date time' not in df.columns or 'co2' not in df.columns or 'sensorID' not in df.columns:
            print("Required columns are missing in the CSV file.")
            return

        df['date time'] = pd.to_datetime(df['date time'])
        df = df.sort_values('date time')

        # Set up the figure and axis
        fig, ax = plt.subplots(figsize=(14, 8))

        # Customize the grid and ticks
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
        ax.tick_params(axis='x', rotation=45, labelsize=10)
        ax.tick_params(axis='y', labelsize=10)

        # Labels and title
        ax.set_xlabel('Date and Time', fontsize=12, labelpad=10)
        ax.set_ylabel('CO2 Emission (ppm)', fontsize=12, labelpad=10)
        ax.set_title('Detailed CO2 Emission Report by Sensor', fontsize=14, pad=15)

        # Customize the color cycle
        unique_sensors = df['sensorID'].unique()
        colors = plt.cm.tab10(np.linspace(0, 1, len(unique_sensors)))

        lines = []
        color_cycle = cycle(colors)
        for sensor_id in unique_sensors:
            sensor_data = df[df['sensorID'] == sensor_id]
            color = next(color_cycle)
            line, = ax.plot(sensor_data['date time'], sensor_data['co2'], marker='o', linestyle='-', color=color, linewidth=2.0, markersize=6, label=sensor_id)
            lines.append((line, sensor_data))

        # Define the hover function
        def on_hover(event):
            for line, sensor_data in lines:
                if event.artist == line:
                    ind = event.target.index
                    sensor_id = sensor_data.iloc[ind]['sensorID']
                    co2_emission = sensor_data.iloc[ind]['co2']
                    current_datetime = sensor_data.iloc[ind]['date time']
                    previous_emission = sensor_data.iloc[ind - 1]['co2'] if ind > 0 else co2_emission
                    if previous_emission != 0:
                        change = ((co2_emission - previous_emission) / previous_emission) * 100
                    else:
                        change = 0
                    action = calculate_action(sensor_data, co2_emission, change)
                    event.annotation.set_text(f"{current_datetime}\nCO2: {co2_emission} ppm\nChange: {change:.2f}%\nAction: {action}")

        def calculate_action(sensor_data, co2_emission, change):
            actions = []
            moving_average = sensor_data['co2'].rolling(window=6, min_periods=1).mean()
            if co2_emission < (moving_average.iloc[-1] * 2):
                actions.append("No Action. Normal Health")
            elif co2_emission > (moving_average.iloc[-1] * 2.5):
                actions.append("Reduce number of occupants. All vent fans ON. All doors opened. All windows opened")
            elif co2_emission > (moving_average.iloc[-1] * 2):
                actions.append("Vent fan ON. Door opened. Window opened.")
            return actions[0]

        # Enable cursor with hover functionality
        cursor = mplcursors.cursor(hover=True)
        cursor.connect("add", on_hover)

        # Improve layout and legend
        ax.legend(title='Sensor ID', fontsize=10, title_fontsize='11', loc='best', fancybox=True, framealpha=0.5)
        plt.tight_layout(pad=2.0)
        plt.show()

    except pd.errors.EmptyDataError:
        print("The CSV file is empty or contains no valid data.")
    except FileNotFoundError:
        print("The CSV file was not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")







