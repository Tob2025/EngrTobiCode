import random
import time
import pandas as pd
from sensor import indoor_locations
from ambient_sc import AmbientSimpleComparison
import diary
from ambient_temp_sensor import graph_plot

# Load the ambient temperature data from the CSV file
ambient_temperature_data = pd.read_csv('ambient_temperature_csv.csv')

# Create an instance of the AmbientSimpleComparison class to prompt for temperature thresholds
location = random.choice(indoor_locations)
ambient_comparison = AmbientSimpleComparison(
    name="Ambient Temperature Sensor",
    location=random.choices(indoor_locations),
    ambient_temperature=None  # Set later during the loop
)

# Loop through each row in the CSV file and process the data
for ambient_temp_index in range(len(ambient_temperature_data)):
    # Get the current time
    current_datetime = time.strftime("%Y-%m-%d %H:%M:%S")

    # Get the ambient temperature for the current index from the CSV file
    ambient_temperature = ambient_temperature_data.iloc[ambient_temp_index]['TEMPERATURE']

    # Update location
    location = random.choice(indoor_locations)

    # Set the current ambient temperature in the comparison instance
    ambient_comparison.ambient_temperature = ambient_temperature

    # Compare ambient temperature with thresholds
    ambient_comparison.evaluate_temperature(ambient_temperature)

    # Log the data
    temp_range = diary.Diary.temp_range2
    data = f"{current_datetime}, {location}, {ambient_temperature:.2f}, {temp_range}".split(", ")
    diary.Diary.log_sensor_data.append(data)
    # print(f"Logged data: {data}")

    # Introduce a 2-second latency after processing each CSV row
    time.sleep(2)


# Log the results at the end
diary.log_ambient_temperature()
graph_plot()
