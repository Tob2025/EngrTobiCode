import time
import random
import diary
import pandas as pd
from temp_sensor import TemperatureSensor
from simple_comparison import SimpleComparison
from sensor import indoor_locations
from bodytemp import graph_plot_body_temperature2

# Load the temperature data from the CSV file
temperature_data = pd.read_csv('body_temperature_csv.csv')

# Define updated formulas for temperature calculation based on SENSOR ID
calculation_formulas = {
    "MLX-P": lambda x: -1.2368 * x + 34.03,
    "MLX-R": lambda x: -1.1986 * x + 33.566,
    "RS T-10": lambda x: -1.419 * x + 32.183,
}

# Create an instance of the TemperatureSensor for the main sensor
main_temp_sensor = TemperatureSensor(
    name="Body Temperature Sensor",
    start_time="12:24:00",
    stop_time="12:25:00",
    location=None,
    temperature_data=temperature_data
)

# Ensure the current_temp_index starts at 0
main_temp_sensor.current_temp_index = 0

# Process each row in the CSV
while main_temp_sensor.current_temp_index < len(temperature_data):
    # Retrieve the current row from the temperature data
    current_row = temperature_data.iloc[main_temp_sensor.current_temp_index]
    sensor_id = current_row['SENSOR ID']
    original_temp = current_row['TEMPERATURE']
    distance = current_row['DISTANCE']  # Read distance directly from the CSV

    # Clean SENSOR ID
    sensor_id_stripped = sensor_id.strip()

    # Calculate the new temperature based on the sensor type and distance
    if sensor_id_stripped in calculation_formulas:
        calculated_temp = calculation_formulas[sensor_id_stripped](distance)
    else:
        # If no formula is defined for the SENSOR ID, skip this row
        print(f"Sensor ID {sensor_id_stripped} has no defined formula. Skipping...")
        main_temp_sensor.current_temp_index += 1
        continue

    # Compare the calculated temperature with the original
    temp_difference = calculated_temp - original_temp
    if -2 <= temp_difference <= 2:
        # Set a new random location for this iteration
        main_temp_sensor.location = random.choice(indoor_locations)

        # Start monitoring with the main temperature sensor
        main_temp_sensor.start()

        # Simulate latency
        time.sleep(4)

        # Get the current time for logging
        current_datetime = time.strftime("%Y-%m-%d %H:%M:%S")

        # Print information
        print(
            f"Time: {current_datetime}, Loc: {main_temp_sensor.location}, "
            f"Orig Temp: {original_temp:.2f}°C, Calc Temp: {calculated_temp:.2f}°C, "
            f"Dist: {distance:.2f}m, Diff: {temp_difference:.2f}°C, ID: {sensor_id_stripped}"
        )

        # Use the calculated temperature for further processing
        SimpleComparison.preprocess(calculated_temp)

        # Log the data including the distance
        diary.Diary.log_sensor_data.append([
            current_datetime, main_temp_sensor.location, f"{original_temp:.2f}",
            f"{calculated_temp:.2f}", f"{distance:.2f}", diary.Diary.temp_range, f"{sensor_id_stripped}"
        ])

        print("")  # Add space after each action for better readability

        # Stop monitoring with the main temperature sensor
        main_temp_sensor.stop()
    else:
        print(
            f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}, Sensor ID: {sensor_id_stripped}, "
            f"Diff: {temp_difference:.2f}°C (Out of range). Skipping..."
        )
        print("")

    # Move to the next row
    main_temp_sensor.current_temp_index += 1

# Log the process with the required arguments
diary.log_body_temperature()

# Reload the updated CSV data after logging the new entries
temperature_data = pd.read_csv('body_temperature.csv', encoding='ISO-8859-1')

# Plot the graph using the updated CSV file
graph_plot_body_temperature2()
