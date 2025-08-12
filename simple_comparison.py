from processor import Processor
from communication_action import commAction
from windows_action import adjust_window
import door_action
from robot_action import activate_robot
from heating_system import controlHeatingSystem
import diary
import time
import numpy as np

# Allow default thresholds when user input is not provided
DEFAULT_LOWER_TEMP = float(input("Enter your lowest body temperature: \n"))
DEFAULT_UPPER_TEMP = float(input("Enter your highest body temperature: \n"))

class SimpleComparison(Processor):
    @staticmethod
    def preprocess(data, lower_temp=DEFAULT_LOWER_TEMP, higher_temp=DEFAULT_UPPER_TEMP):
        """
        Preprocesses temperature data and performs actions based on predefined thresholds.

        Args:
            data (float): The temperature data to be processed.
            lower_temp (float): The lower threshold for temperature comparison.
            higher_temp (float): The upper threshold for temperature comparison.
        """
        if lower_temp is None or higher_temp is None:
            lower_temp = DEFAULT_LOWER_TEMP
            higher_temp = DEFAULT_UPPER_TEMP

        if lower_temp <= data <= higher_temp:
            print(f'Body Temperature: {data:.2f}°C (Normal Body Temperature)')
            remark = "Normal Body Temperature"
            diary.Diary.temp_range = remark
        elif data < lower_temp:
            print(f'Body Temperature: {data:.2f}°C (Low Temperature)')
            door_action.closeDoor()
            time.sleep(3)
            controlHeatingSystem()
            time.sleep(3)
            activate_robot()
            time.sleep(np.random.uniform(3, 9))
            remark = "Low Temperature"
            diary.Diary.temp_range = remark
        elif data > higher_temp:
            print(f'Body Temperature: {data:.2f}°C (High Temperature)')
            door_action.openDoor()
            time.sleep(3)
            controlHeatingSystem()
            time.sleep(3)
            commAction()
            time.sleep(3)
            adjust_window()
            time.sleep(np.random.uniform(3, 9))
            remark = "High Temperature"
            diary.Diary.temp_range = remark
        else:
            print(f'Body Temperature: {data:.2f}°C (Temperature within specified range)')
            remark = "Temperature within specified range"
            diary.Diary.temp_range = remark

# Optional utility function for explicit user input when needed
def prompt_for_thresholds():
    """
    Prompts the user for low and high temperature thresholds.

    Returns:
        tuple: A tuple containing lower and upper temperature thresholds.
    """
    lower_temp = float(input("Enter your lowest body temperature: \n"))
    higher_temp = float(input("Enter your highest body temperature: \n"))
    return lower_temp, higher_temp
