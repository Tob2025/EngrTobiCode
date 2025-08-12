from sensor import Sensor
from detect_person_processor import DetectPersonProcessor

class MotionSensor(Sensor):
    def __init__(self, name, start_time, stop_time=None, location=None):
        super().__init__(
            name=name,
            datatype="float",
            start_time=start_time,
            stop_time=stop_time,
            location=location
        )

    @staticmethod
    def noMotionDetected():
        print("No motion detected.")

    @staticmethod
    def motionDetected():
        DetectPersonProcessor.conditions()
