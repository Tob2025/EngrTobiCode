import time
import numpy as np
import door_action
import diary
from temp_sensor import TemperatureSensor
from commAction import comm_action
from heating_system import controlHeatingSystem
from robot_action import activate_robot
from windows_action import adjust_window

class AmbientSimpleComparison(TemperatureSensor):
    def __init__(self, name, location, ambient_temperature):
        lower_threshold = float(input("Enter your lowest ambient room temperature: \n"))
        upper_threshold = float(input("Enter your highest ambient room temperature: \n"))
        super().__init__(name=name, location=location, start_time=None, stop_time=None, temperature_data=None)
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold

    def evaluate_temperature(self, data):
        """
        Evaluates the ambient temperature and performs actions based on predefined thresholds.

        Args:
            data (float): The current ambient temperature.
        """
        if data < self.lower_threshold:
            self.handle_low_temperature(data)
        elif data > self.upper_threshold:
            self.handle_high_temperature(data)
        else:
            self.handle_normal_temperature(data)

    def handle_low_temperature(self, data):
        """
        Handles actions when the temperature is below the lower threshold.

        Args:
            data (float): The current ambient temperature.
        """
        print(f'Ambient Temperature: {data:.2f}°C (Low Temperature)')
        door_action.closeDoor()
        controlHeatingSystem()
        activate_robot()
        time.sleep(np.random.uniform(3, 9))
        remark = "Low Temperature"
        diary.Diary.temp_range2 = remark
        print("")

    def handle_high_temperature(self, data):
        """
        Handles actions when the temperature is above the upper threshold.

        Args:
            data (float): The current ambient temperature.
        """
        print(f'Ambient Temperature: {data:.2f}°C (High Temperature)')
        door_action.openDoor()
        controlHeatingSystem()
        comm_action()
        adjust_window()
        time.sleep(np.random.uniform(3, 9))
        remark = "High Temperature"
        diary.Diary.temp_range2 = remark
        print("")

    def handle_normal_temperature(self, data):
        """
        Handles actions when the temperature is within the normal range.

        Args:
            data (float): The current ambient temperature.
        """
        print(f'Ambient Temperature: {data:.2f}°C (Temperature within specified range)')
        remark = "Temperature within specified range"
        diary.Diary.temp_range2 = remark
        print("")
