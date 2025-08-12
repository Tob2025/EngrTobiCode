import time
from detect_person_processor import DetectPersonProcessor
import diary

duration_seconds = 120

start_time = time.time()

while time.time() - start_time <= duration_seconds:
    DetectPersonProcessor.conditions()

diary.log_motion_sensor()
