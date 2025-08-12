import time, co2_processor_2, diary
from co2_processor_2 import graph_plot

duration_seconds = 5

st = time.time()

while time.time() - st <= duration_seconds:
    co2_processor_2.CO2Processor.process_conditions()

diary.log_co2_emission()
graph_plot()

