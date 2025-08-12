import time
import random
import diary
import pandas as pd
from temp_sensor import TemperatureSensor
from simple_comparison import SimpleComparison
from sensor import indoor_locations
from bodytemp import graph_plot_body_temperature

# Load the temperature data from the CSV file
temperature_data = pd.read_csv('body_temperature_csv.csv')

# Create an instance of the TemperatureSensor for the main sensor
main_temp_sensor = TemperatureSensor(
    name="Body Temperature Sensor",
    start_time="12:24:00",
    stop_time="12:25:00",
    location=None,  # Will be set dynamically during the loop
    temperature_data=temperature_data  # Pass the CSV data to the sensor
)

# Run the simulation through the entire CSV data
while main_temp_sensor.current_temp_index < len(temperature_data):
    # Set a new random location for each iteration
    main_temp_sensor.location = random.choice(indoor_locations)

    # Start monitoring with the main temperature sensor
    main_temp_sensor.start()

    # Collect data from the main sensor
    main_temp_data = main_temp_sensor.getdata()
    time.sleep(4)

    # Print data from the main sensor, including the new random location
    current_datetime = time.strftime("%Y-%m-%d %H:%M:%S")

    print(
        f"Time: {current_datetime}, Location: {main_temp_sensor.location}, Temperature: {main_temp_data:.2f} °C, Datatype: {main_temp_sensor.datatype}"
    )

    SimpleComparison.preprocess(main_temp_data)
    diary.Diary.log_sensor_data.append([
        current_datetime, main_temp_sensor.location, f"{main_temp_data:.2f}", diary.Diary.temp_range
    ])

    print("")

    # Stop monitoring with the main temperature sensor
    main_temp_sensor.stop()

# Log the process with the required arguments
diary.log_body_temperature()

# Reload the updated CSV data after logging the new entries
temperature_data = pd.read_csv('body_temperature.csv',encoding='ISO-8859-1')

# Plot the graph using the updated CSV file
graph_plot_body_temperature()