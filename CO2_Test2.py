import time, co2_processor_3, diary
from co2_processor_3 import graph_plot

duration_seconds = 5

st = time.time()

while time.time() - st <= duration_seconds:
    co2_processor_3.C02_Processor.conditions()

diary.log_co2_emission()
graph_plot()

