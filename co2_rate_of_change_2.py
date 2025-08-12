import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


class CO2DataAnalyzer:
    def __init__(self, input_file, output_file, target_sensor):
        self.input_file = input_file
        self.output_file = output_file
        self.target_sensor = target_sensor.strip()
        self.fixed_interval = 10  # Hardcoded 10-minute assumption

    def process_data(self):
        """Process data with fixed 10-minute intervals between readings"""
        try:
            with open(self.input_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                if not all(col in reader.fieldnames for col in ["sensorID", "co2", "date time"]):
                    raise ValueError("CSV missing required columns")

                processed = []
                previous_co2 = None

                for row in reader:
                    if row["sensorID"].strip() == self.target_sensor:
                        try:
                            current_co2 = float(row["co2"])
                            rate = None

                            if previous_co2 is not None:
                                # Use fixed 10-minute interval
                                co2_diff = current_co2 - previous_co2
                                rate = co2_diff / self.fixed_interval

                            processed.append({
                                "sensorID": self.target_sensor,
                                "co2": current_co2,
                                "date time": row["date time"].strip(),  # Keep original timestamp
                                "rate_of_change": rate
                            })

                            previous_co2 = current_co2

                        except (ValueError, KeyError) as e:
                            print(f"Skipping invalid row: {e}")

            if processed:
                with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=["sensorID", "co2", "date time", "rate_of_change"])
                    writer.writeheader()
                    writer.writerows(processed)
                print(f"Data saved to {self.output_file}")
            else:
                print(f"No data for sensor: {self.target_sensor}")

        except Exception as e:
            print(f"Processing failed: {e}")

    def visualize_trends(self):
        """Visualize CO2 change rates with 10-minute assumption"""
        try:
            df = pd.read_csv(self.output_file, parse_dates=["date time"])
            df = df.dropna(subset=["rate_of_change"])

            if df.empty:
                print("No data for visualization")
                return

            plt.figure(figsize=(14, 7))
            plt.plot(df["date time"], df["rate_of_change"],
                     marker='o', linestyle='-', color='#e67e22', linewidth=2)

            plt.title(f"CO2 Rate of Change (10-Minute Intervals)\nSensor: {self.target_sensor}", fontsize=14)
            plt.xlabel("Date Time", fontsize=12)
            plt.ylabel("Rate of Change (ppm/minute)", fontsize=12)

            plt.gcf().autofmt_xdate()
            plt.grid(True, alpha=0.4)
            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Visualization error: {e}")


if __name__ == "__main__":
    configurations = [
        {
            "input_file": "co2_data1.csv",
            "output_file": "co2_analysis_results_1.csv",
            "target_sensor": "lw-ms-ambi-03"
        },
        {
            "input_file": "co2_data2.csv",
            "output_file": "co2_analysis_results_2.csv",
            "target_sensor": "lw-ms-ambi-03"
        },
        {
            "input_file": "co2_data3.csv",
            "output_file": "co2_analysis_results_3.csv",
            "target_sensor": "lw-ms-ambi-01"
        }
    ]

    for config in configurations:
        analyzer = CO2DataAnalyzer(
            input_file=config["input_file"],
            output_file=config["output_file"],
            target_sensor=config["target_sensor"]
        )
        analyzer.process_data()
        analyzer.visualize_trends()