from sensor import Sensor


class CO2Monitoring(Sensor):
    def __init__(self, location, timestamp, name, datatype, start_time, stop_time):
        super().__init__(name, datatype, start_time, location)
        self.location = location
        self.timestamp = timestamp
        self.start_time = start_time
        self.stop_time = stop_time

    def __str__(self):
        return (f"CO2Monitoring Sensor: {self.name}, Location: {self.location}, Timestamp: {self.timestamp}, "
                f"Data Type: {self.datatype}, Start Time: {self.start_time}, Stop Time: {self.stop_time}")
