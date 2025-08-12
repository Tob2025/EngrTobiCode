import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import mplcursors


class Actions:
    @staticmethod
    def take_action(status):
        if status == "Out of Range":
            print("Action Triggered!")
        else:
            print("Normal")


def parse_sensor_data(csv_file):
    """Parse sensor data from CSV files"""
    if not os.path.isfile(csv_file):
        raise FileNotFoundError(f"File '{csv_file}' not found")

    df = pd.read_csv(csv_file, header=None)
    sensors = {}
    current_sensor = None
    distances = []
    data_rows = []
    expecting_distances = False

    for _, row in df.iterrows():
        if pd.notna(row[1]) and ('MLX' in row[1] or 'RS-T10' in row[1]):
            if current_sensor:
                data_df = pd.DataFrame(data_rows, columns=distances)
                data_df.set_index('AmbientTemp', inplace=True)
                data_df = data_df.interpolate(method='linear', axis=0).interpolate(method='linear', axis=1)
                sensors[current_sensor] = data_df
                data_rows = []
                distances = []
            current_sensor = row[1]
            expecting_distances = True
            continue

        if expecting_distances:
            distances = ['AmbientTemp'] + [float(str(col).replace('m', '')) for col in row[1:6]]
            expecting_distances = False
            continue

        if pd.notna(row[0]):
            try:
                ambient_temp = float(row[0])
                values = []
                for i in range(1, 6):
                    cell_value = row[i]
                    try:
                        val = float(str(cell_value)) if pd.notna(cell_value) else np.nan
                    except ValueError:
                        val = np.nan
                    values.append(val)
                data_rows.append([ambient_temp] + values)
            except ValueError:
                continue

    if current_sensor:
        data_df = pd.DataFrame(data_rows, columns=distances)
        data_df.set_index('AmbientTemp', inplace=True)
        data_df = data_df.interpolate(method='linear', axis=0).interpolate(method='linear', axis=1)
        sensors[current_sensor] = data_df

    return sensors


def bilinear_interpolation(x, y, x_coords, y_coords, z_grid):
    """Perform bilinear interpolation"""
    x_idx = np.searchsorted(x_coords, x) - 1
    if x_idx < 0:
        x_idx = 0
    elif x_idx >= len(x_coords) - 1:
        x_idx = len(x_coords) - 2
    x1, x2 = x_coords[x_idx], x_coords[x_idx + 1]

    y_idx = np.searchsorted(y_coords, y) - 1
    if y_idx < 0:
        y_idx = 0
    elif y_idx >= len(y_coords) - 1:
        y_idx = len(y_coords) - 2
    y1, y2 = y_coords[y_idx], y_coords[y_idx + 1]

    Q11 = z_grid[y_idx, x_idx]
    Q12 = z_grid[y_idx + 1, x_idx]
    Q21 = z_grid[y_idx, x_idx + 1]
    Q22 = z_grid[y_idx + 1, x_idx + 1]

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0: return Q11
    if dx == 0: return (Q11 * (y2 - y) + Q12 * (y - y1)) / dy
    if dy == 0: return (Q11 * (x2 - x) + Q21 * (x - x1)) / dx

    f_y1 = ((x2 - x) / dx) * Q11 + ((x - x1) / dx) * Q21
    f_y2 = ((x2 - x) / dx) * Q12 + ((x - x1) / dx) * Q22
    return ((y2 - y) / dy) * f_y1 + ((y - y1) / dy) * f_y2


def plot_2d(sensor_name, df, data_type):
    """Plot 2D line graph for sensor data"""
    plt.figure(figsize=(12, 7))

    ambient_temps = df.index.values
    distances = df.columns.astype(float).values
    colors = plt.cm.viridis(np.linspace(0, 1, len(ambient_temps)))

    # Plot lines for each ambient temperature
    for temp, color in zip(ambient_temps, colors):
        plt.plot(distances,
                 df.loc[temp].values,
                 color=color,
                 linewidth=2,
                 marker='o',
                 markersize=6,
                 label=f'{temp:.1f}°C')

    # Configure axis
    plt.xlabel('Distance (m)', fontsize=12, fontweight='bold')
    plt.ylabel(f'{data_type} Temperature (°C)', fontsize=12, fontweight='bold')
    plt.title(f'{sensor_name} {data_type} Temperature Profile', fontsize=14, fontweight='bold')

    # Create colorbar with explicit axes reference
    ax = plt.gca()
    sm = plt.cm.ScalarMappable(cmap='viridis',
                               norm=plt.Normalize(vmin=min(ambient_temps),
                                                  vmax=max(ambient_temps)))
    sm.set_array([])  # Required for empty array initialization
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Ambient Temperature (°C)', fontsize=10)

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def run_scenario():
    """Run smart home monitoring scenario visualization"""
    data_points = [
        {
            'time': '07:00',
            'room': 'Bedroom',
            'ambient_temp': 21.0,
            'distance': 1.1,
            'measured_temp': 36.5,
            'interpolated_temp': 36.76,
            'stddev': 0.19,
            'acceptable_range': '36.57 to 36.95',
            'status': 'Normal',
            'action': 'Routine logging'
        },
        {
            'time': '08:00',
            'room': 'Kitchen',
            'ambient_temp': 25.2,
            'distance': 1.5,
            'measured_temp': 37.2,
            'interpolated_temp': 36.91,
            'stddev': 0.23,
            'acceptable_range': '36.68 to 37.14',
            'status': 'Normal',
            'action': 'Routine logging'
        },
        {
            'time': '09:00',
            'room': 'Living Room',
            'ambient_temp': 25.7,
            'distance': 2.0,
            'measured_temp': 37.0,
            'interpolated_temp': 36.68,
            'stddev': 0.26,
            'acceptable_range': '36.42 to 36.94',
            'status': 'Abnormal',
            'action': 'Alert GP, adjust HVAC, dispatch robot'
        },
        {
            'time': '10:00',
            'room': 'Study',
            'ambient_temp': 29.0,
            'distance': 1.2,
            'measured_temp': 37.3,
            'interpolated_temp': 37.12,
            'stddev': 0.21,
            'acceptable_range': '36.91 to 37.33',
            'status': 'Normal',
            'action': 'Routine logging'
        }
    ]

    # Save scenario data to CSV
    df = pd.DataFrame(data_points)
    df.to_csv('scenario_log.csv', index=False)
    print("Scenario data logged to 'scenario_log.csv'")

    ambient_temp = [point['ambient_temp'] for point in data_points]
    distance = [point['distance'] for point in data_points]
    times = [point['time'] for point in data_points]

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(ambient_temp, distance, 'b--', alpha=0.5, marker='', label='Time progression')

    scatter = ax.scatter(
        ambient_temp, distance,
        c='blue',
        s=100,
        edgecolor='black',
        zorder=3
    )

    ax.set_xlabel('Ambient Temperature (°C)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Distance (m)', fontsize=12, fontweight='bold')
    ax.set_title('Smart Home Monitoring: Ambient Temperature vs Camera Distance\nMrs. Lee\'s Morning Activity',
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_xlim(20, 30)
    ax.set_ylim(1.0, 2.1)
    ax.legend()

    cursor = mplcursors.cursor(scatter, hover=True)

    @cursor.connect("add")
    def on_hover(sel):
        idx = sel.index
        data = data_points[idx]
        annotation_text = (
            f"Time: {data['time']}\n"
            f"Room: {data['room']}\n"
            f"Ambient Temp: {data['ambient_temp']}°C\n"
            f"Distance: {data['distance']}m\n"
            f"Measured Temp: {data['measured_temp']}°C\n"
            f"Interpolated Temp: {data['interpolated_temp']}°C\n"
            f"Std Deviation: ±{data['stddev']}°C\n"
            f"Acceptable Range: {data['acceptable_range']}\n"
            f"Status: {data['status']}\n"
            f"System Action: {data['action']}"
        )
        sel.annotation.set_text(annotation_text)
        sel.annotation.get_bbox_patch().set(
            boxstyle="round,pad=0.5",
            fc="white", alpha=0.9, edgecolor="black"
        )
        sel.annotation.set_fontsize(10)

    plt.tight_layout()
    plt.show()


def main():
    print("=== Sensor Temperature Analysis ===")

    try:
        # Load both datasets
        mean_data = parse_sensor_data("bi-linear_tables.csv")
        std_data = parse_sensor_data("bi-linear_tables_2.csv")
        sensors = {name: {'mean': mean_data[name], 'std': std_data[name]}
                   for name in mean_data}
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # 2D Visualization
    if input("\nGenerate 2D visualizations? (y/n): ").lower() == 'y':
        for sensor_name in sensors:
            print(f"\nGenerating 2D plots for {sensor_name}...")
            plot_2d(sensor_name, sensors[sensor_name]['mean'], 'Mean')
            plot_2d(sensor_name, sensors[sensor_name]['std'], 'Standard Deviation')

    # Measurement Analysis
    if input("\nAnalyze measurements? (y/n): ").lower() == 'y':
        file_name = input("Enter data filename: ").strip()
        sensor_name = input("Enter sensor (MLX-P/MLX-R/RS-T10): ").strip()

        if sensor_name not in sensors:
            print(f"Invalid sensor: {sensor_name}")
            return

        try:
            new_data = pd.read_csv(file_name)
            required_columns = {'Distance', 'AmbientTemp', 'MeasuredTemp'}
            if not required_columns.issubset(new_data.columns):
                missing = required_columns - set(new_data.columns)
                raise ValueError(f"Missing columns: {missing}")

            results = []
            for _, row in new_data.iterrows():
                try:
                    distance = float(row['Distance'])
                    ambient_temp = float(row['AmbientTemp'])
                    measured_temp = float(row['MeasuredTemp'])
                except ValueError:
                    raise ValueError("Non-numeric values in input data")

                mean_val = bilinear_interpolation(
                    distance, ambient_temp,
                    sensors[sensor_name]['mean'].columns.astype(float),
                    sensors[sensor_name]['mean'].index.astype(float),
                    sensors[sensor_name]['mean'].values
                )

                std_val = bilinear_interpolation(
                    distance, ambient_temp,
                    sensors[sensor_name]['std'].columns.astype(float),
                    sensors[sensor_name]['std'].index.astype(float),
                    sensors[sensor_name]['std'].values
                )

                diff = measured_temp - mean_val
                status = "Within Range" if -2 <= diff <= 2 else "Out of Range"

                if status == "Out of Range":
                    Actions.take_action(status)

                results.append({
                    'Sensor': sensor_name,
                    'Distance': distance,
                    'AmbientTemp': ambient_temp,
                    'MeasuredTemp': measured_temp,
                    'MeanTemp': mean_val,
                    'StdDev': std_val,
                    'Difference': diff,
                    'Status': status
                })

            results_df = pd.DataFrame(results)
            results_df.to_csv('interpolated_results.csv', index=False)
            print("\nResults saved to interpolated_results.csv")

            # Create interactive plot with swapped axes
            plt.figure(figsize=(12, 7))
            results_df = results_df.sort_values(['AmbientTemp', 'Distance']).reset_index(drop=True)

            line = plt.plot(
                results_df['AmbientTemp'],  # X-axis now ambient temperature
                results_df['Distance'],  # Y-axis now distance
                marker='o',
                markersize=8,
                linestyle='-',
                linewidth=2,
                color='#1f77b4',
                markerfacecolor='white',
                markeredgewidth=1.5
            )

            ax = plt.gca()
            ax.xaxis.set_major_locator(plt.MultipleLocator(0.5))
            ax.xaxis.set_minor_locator(plt.MultipleLocator(0.25))
            ax.yaxis.set_major_locator(plt.MultipleLocator(0.2))
            ax.yaxis.set_minor_locator(plt.MultipleLocator(0.1))

            ax.xaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
            ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))

            plt.xlabel('Ambient Temperature (°C)', fontsize=12, fontweight='bold')
            plt.ylabel('Distance (m)', fontsize=12, fontweight='bold')
            plt.title('Measurement Analysis: Ambient Temperature vs Distance',
                      fontsize=14, fontweight='bold', pad=20)
            plt.grid(True, linestyle='--', alpha=0.7)

            # Hover functionality
            cursor = mplcursors.cursor(line[0], hover=True)

            def update_annotation(sel):
                idx = sel.index
                row = results_df.iloc[idx]
                annotation_text = (
                    f"Sensor: {row['Sensor']}\n"
                    f"Distance: {row['Distance']:.2f}m\n"
                    f"Ambient Temp: {row['AmbientTemp']:.2f}°C\n"
                    f"Measured Temp: {row['MeasuredTemp']:.2f}°C\n"
                    f"Mean Reference: {row['MeanTemp']:.2f}°C\n"
                    f"Std Deviation: {row['StdDev']:.2f}°C\n"
                    f"Difference: {row['Difference']:.2f}°C\n"
                    f"Status: {row['Status']}\n"
                    f"Action: {'Windows, Doors and Comm Actions Required' if row['Status'] == 'Out of Range' else 'Normal'}"
                )
                sel.annotation.set_text(annotation_text)
                sel.annotation.get_bbox_patch().set(
                    fc="white",
                    alpha=0.95,
                    boxstyle="round,pad=0.3"
                )
                sel.annotation.set_fontsize(10)
                sel.annotation.set_ha('left')

            cursor.connect("add", update_annotation)
            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"\nERROR: {str(e)}")
            print("Ensure input CSV contains correct columns with numeric values.")

    # Smart Home Scenario
    if input("\nRun smart home monitoring scenario? (y/n): ").lower() == 'y':
        print("\nRunning smart home scenario visualization...")
        run_scenario()


if __name__ == "__main__":
    main()