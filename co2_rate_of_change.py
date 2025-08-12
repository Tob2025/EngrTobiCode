import csv
import pandas as pd
import matplotlib.pyplot as plt


class CO2Processor:
    def __init__(self, input_file, output_file, sensor_id):
        self.input_file = input_file
        self.output_file = output_file
        self.sensor_id = sensor_id.strip()  # Target sensor ID (e.g., "lw-ms-ambi-01")
        self.MINUTES_PER_YEAR = 525600  # 60 min * 24 hrs * 365 days

    def process_data(self):
        try:
            # Read input CSV and filter data
            with open(self.input_file, mode="r", newline="", encoding="utf-8") as infile:
                reader = csv.DictReader(infile)

                # Check required columns
                if "sensorID" not in reader.fieldnames or "co2" not in reader.fieldnames:
                    raise KeyError("CSV must contain 'sensorID' and 'co2' columns.")

                filtered_data = []
                for row in reader:
                    # Filter rows by sensorID and validate co2
                    if row["sensorID"].strip() == self.sensor_id:
                        try:
                            co2_value = float(row["co2"])
                            filtered_data.append({
                                "sensorID": row["sensorID"].strip(),
                                "co2": co2_value
                            })
                        except ValueError:
                            print(f"Skipped invalid CO2 value: {row['co2']}")

            # Calculate rate_of_change (ppm/year) for consecutive data points
            for i in range(len(filtered_data)):
                if i == 0:
                    # First row has no previous data, so rate is None
                    filtered_data[i]["rate_of_change"] = None
                else:
                    delta_co2 = filtered_data[i]["co2"] - filtered_data[i - 1]["co2"]
                    # Time interval is fixed at 10 minutes
                    rate_ppm_per_year = delta_co2 * (self.MINUTES_PER_YEAR / 10)  # ppm/year
                    filtered_data[i]["rate_of_change"] = rate_ppm_per_year

            # Write to output CSV
            if filtered_data:
                with open(self.output_file, mode="w", newline="", encoding="utf-8") as outfile:
                    writer = csv.DictWriter(outfile, fieldnames=["sensorID", "co2", "rate_of_change"])
                    writer.writeheader()
                    writer.writerows(filtered_data)
                print(f"Data saved to '{self.output_file}' with {len(filtered_data)} rows.")
            else:
                print(f"No data found for sensorID '{self.sensor_id}'.")

        except FileNotFoundError:
            print(f"Error: File '{self.input_file}' not found.")
        except KeyError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def plot_co2_trend(self):
        try:
            df = pd.read_csv(self.output_file)
            if df.empty:
                print("No data to plot.")
                return

            # Plot CO2 and rate of change
            fig, (ax2) = plt.subplots(1, 1, figsize=(12, 8))

            # # Plot CO2 data
            # ax1.plot(df["co2"], marker="o", linestyle="-", color="tab:blue")
            # ax1.set_title(f"CO2 Concentration ({self.sensor_id})")
            # ax1.set_ylabel("CO2 (ppm)")
            # ax1.grid(True)

            # Plot rate of change (skip first NaN value)
            ax2.plot(df["rate_of_change"].iloc[1:], marker="o", linestyle="-", color="tab:red")
            ax2.set_title("Rate of Change (ppm/year)")
            ax2.set_xlabel("Measurement Index")
            ax2.set_ylabel("Rate (ppm/year)")
            ax2.grid(True)

            plt.tight_layout()
            plt.show()

        except FileNotFoundError:
            print(f"Error: File '{self.output_file}' not found.")
        except Exception as e:
            print(f"Plotting error: {e}")



if __name__ == "__main__":
    processor = CO2Processor(
        input_file="co2_data1.csv",
        output_file="filtered_co2_data.csv",
        sensor_id="lw-ms-ambi-01"  # Correct sensor ID
    )
    processor.process_data()
    processor.plot_co2_trend()
