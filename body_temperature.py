import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def parse_sensor_data(csv_file):
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
            distances = ['AmbientTemp'] + [float(str(col).replace('m', '')) for col in row[1:6] if pd.notna(col)]
            expecting_distances = False
            continue

        if pd.notna(row[0]) and str(row[0]).replace('.','').isdigit():
            try:
                ambient_temp = float(row[0])
                values = []
                for i in range(1, min(len(row), len(distances))):
                    cell_value = row[i]
                    try:
                        val = float(str(cell_value)) if pd.notna(cell_value) else np.nan
                    except ValueError:
                        val = np.nan
                    values.append(val)
                if len(values) == len(distances) - 1:
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

def plot_body_temperature_analysis(df):
    try:
        df['datetime'] = pd.to_datetime('2024-01-01 ' + df['time'].astype(str))
        time_values = df['datetime']
        use_datetime = True
    except:
        if ':' in str(df['time'].iloc[0]):
            time_values = [float(t.split(':')[0]) + float(t.split(':')[1]) / 60 for t in df['time']]
        else:
            time_values = df.index.values
        use_datetime = False
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    measured_temps = df['measured_body_temp_c']
    interpolated_means = df['mean_temp_c']  
    ax.plot(time_values, measured_temps, 'ro-', linewidth=1.5, markersize=5, 
            label='Measured Body Temperature')
    ax.plot(time_values, interpolated_means, 'bs--', linewidth=1.5, markersize=5,
            label='Body Temperature')
    
    abnormal = df[df['within_range'] == 'No']
    if not abnormal.empty:
        if use_datetime:
            abn_times = pd.to_datetime('2024-01-01 ' + abnormal['time'].astype(str))
        else:
            abn_times = [float(t.split(':')[0]) + float(t.split(':')[1])/60 
                         for t in abnormal['time']]
        
        ax.scatter(abn_times, abnormal['measured_body_temp_c'], 
                   color='orange', s=100, marker='x', linewidth=2, 
                   label='Abnormal Readings', zorder=10)
    
    # Format plot
    ax.set_ylabel('Temperature (°C)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Time (per hour)', fontsize=12, fontweight='bold')
    ax.set_title('Body Temperature Monitoring Analysis', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', framealpha=0.8)  
    if use_datetime:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
        plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('body_temperature_analysis.png', dpi=300, bbox_inches='tight')
    print("Plot saved as 'body_temperature_analysis.png'")
    plt.show()

def process_body_temperature_data():
    try:
        mean_data = parse_sensor_data('bi-linear_tables.csv')
        std_data = parse_sensor_data('bi-linear_tables_2.csv')
        sensors = {name: {'mean': mean_data[name], 'std': std_data[name]}
                   for name in mean_data}
    except FileNotFoundError as e:
        print(f"Error loading sensor tables: {e}")
        return
    
    available_sensors = list(sensors.keys())
    print("\nAvailable sensors:")
    for i, sensor in enumerate(available_sensors):
        print(f"{i + 1}. {sensor}")
    
    while True:
        try:
            choice = input(f"Select sensor (1-{len(available_sensors)}): ").strip()
            sensor_idx = int(choice) - 1
            if 0 <= sensor_idx < len(available_sensors):
                sensor_name = available_sensors[sensor_idx]
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    
    try:
        df = pd.read_csv('body_temperature1.csv')
        print(f"Loaded {len(df)} records from body_temperature2.csv")
    except FileNotFoundError:
        print(f"Error: body_temperature1.csv not found")
        return
    
    processed_data = []
    
    for idx, row in df.iterrows():
        try:
            time = row['time']
            room = row['room']
            distance = float(row['distance_m'])
            ambient_temp = float(row['ambient_temp_c'])
            measured_temp = float(row['measured_body_temp_c'])
            
            # Calculate interpolated mean (body temperature)
            interpolated_mean = bilinear_interpolation(
                distance, ambient_temp,
                sensors[sensor_name]['mean'].columns.astype(float),
                sensors[sensor_name]['mean'].index.astype(float),
                sensors[sensor_name]['mean'].values
            )
            
            # Calculate interpolated standard deviation
            interpolated_std = bilinear_interpolation(
                distance, ambient_temp,
                sensors[sensor_name]['std'].columns.astype(float),
                sensors[sensor_name]['std'].index.astype(float),
                sensors[sensor_name]['std'].values
            )
            
            lower_bound = interpolated_mean - interpolated_std
            upper_bound = interpolated_mean + interpolated_std
            
            within_range = "Yes" if lower_bound <= measured_temp <= upper_bound else "No"
            
            if within_range == "Yes":
                action_taken = "Routine logging"
            else:
                action_taken = "Alert GP, adjust HVAC, dispatch robot"
            
            processed_data.append({
                'time': time,
                'room': room,
                'distance_m': distance,
                'ambient_temp_c': ambient_temp,
                'measured_body_temp_c': measured_temp,
                'body_temp': round(interpolated_mean, 2),  # Store interpolated mean
                'mean_temp_c': round(interpolated_mean, 2),  # Same as body_temp (for compatibility)
                'standard_dev': round(interpolated_std, 2),
                'within_range': within_range,
                'action_taken': action_taken
            })
            
        except Exception as e:
            print(f"Error processing row {idx}: {e}")
            continue
    
    if processed_data:
        result_df = pd.DataFrame(processed_data)
        output_file = 'body_temperature_processed.csv'
        result_df.to_csv(output_file, index=False)
        
        print(f"\nProcessed data saved to '{output_file}'")
        print(f"Total records processed: {len(processed_data)}")
        
        plot_body_temperature_analysis(result_df)
        
        normal_count = sum(1 for row in processed_data if row['within_range'] == 'Yes')
        abnormal_count = len(processed_data) - normal_count
        
        print(f"Normal readings: {normal_count}")
        print(f"Abnormal readings: {abnormal_count}")
        print(f"Actions triggered: {abnormal_count}")
        
        print(f"\nUsing sensor: {sensor_name}")
        
        return result_df
    else:
        print("No data could be processed")
        return None

if __name__ == "__main__":
    result = process_body_temperature_data()