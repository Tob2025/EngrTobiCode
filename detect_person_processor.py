import communication_action
import windows_action
import door_action
import time
import diary
import random
from sensor import indoor_locations, positions, moving_pattern
from robot_action import activate_robot
from processor import Processor


def perform_actions():
    time.sleep(2)
    communication_action.commAction()
    time.sleep(2)
    windows_action.adjust_window()
    time.sleep(2)
    door_action.adjustDoor()
    print("")
    print("")


class DetectPersonProcessor(Processor):
    @staticmethod
    def conditions():
        current_datetime = time.strftime("%Y-%m-%d %H:%M:%S")
        location = random.choice(indoor_locations)
        position = random.choice(positions)
        pattern = random.choice(moving_pattern)

        def log_data(health_status):
            data = [current_datetime, location, pattern, position, health_status]
            diary.Diary.log_sensor_data.append(data)
            print(f"""
                Health status at {current_datetime} in the {location} is {health_status}
                Position = {position}
                Movement Pattern = {pattern}
            """)
            time.sleep(4)

        def log_abnormal_status():
            log_data("Abnormal")
            perform_actions()

        print(f"Current Location: {location}")
        activate_robot()
        time.sleep(3)

        if location == "Living Room":
            if position in ["Sitting", "Lying on couch", "Standing"]:
                if pattern == 'Normal':
                    log_data("Normal")
                else:
                    log_abnormal_status()
            else:
                log_abnormal_status()

        elif location == "Kitchen":
            ambient_temp = random.randrange(18, 26)
            if pattern == "Normal":
                if 18 <= ambient_temp <= 20:
                    if position in ["Standing", "Sitting"]:
                        log_data("Normal")
                    else:
                        log_abnormal_status()
                        communication_action.commAction()
                        print("")
                else:
                    log_abnormal_status()
                    communication_action.commAction()
                    print("")
            else:
                log_abnormal_status()

        elif location in ["Toilet", "Bathroom"]:
            position = random.choice(["Sitting", "Standing", "Lying down"])
            if position in ["Sitting", "Standing"]:
                if pattern == "Normal":
                    time_spent = random.randint(2, 41)
                    if time_spent <= 30:
                        log_data("Normal")
                    else:
                        log_abnormal_status()
                else:
                    log_abnormal_status()
            else:
                log_abnormal_status()
                communication_action.commAction()
                print("")

        elif location == "Bedroom":
            position = random.choice(["Sitting", "Standing", "Lying on the floor", "Lying on couch", "Lying in bed"])
            if position in ["Sitting", "Lying in bed", "Standing", "Lying on couch"]:
                if pattern == 'Normal':
                    log_data("Normal")
                else:
                    log_abnormal_status()
            else:
                log_abnormal_status()

        elif location in ["Staircase", "Passage"]:
            if pattern == "Normal" and position == "Standing":
                log_data("Normal")
            else:
                log_abnormal_status()

        elif location == "Office":
            if pattern == "Normal" and position in ["Sitting", "Standing"]:
                log_data("Normal")
            else:
                log_abnormal_status()

        else:
            log_abnormal_status()
