import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

def plot_combined_temperature_data(csv_files, room_names, colors, time_column='time', temp_column='temp_c'):
    
    plt.figure(figsize=(14, 8))
    
    all_temps = []
    all_times = []
    
    for i, (csv_file, room_name, color) in enumerate(zip(csv_files, room_names, colors)):
        try:
            df = pd.read_csv(csv_file)
            print(f"Successfully loaded data from {csv_file}")
            print(f"Data shape: {df.shape}")
            
            df['datetime'] = pd.to_datetime('2024-01-01 ' + df[time_column].astype(str))
            df[temp_column] = pd.to_numeric(df[temp_column], errors='coerce')
            
            plt.plot(df['datetime'], df[temp_column], 
                    color=color, linewidth=2, marker='o', markersize=2, 
                    label=f'{room_name}', alpha=0.8)
            
            all_temps.extend(df[temp_column].dropna().tolist())
            all_times.extend(df['datetime'].tolist())
            
            print(f"{room_name} - Min: {df[temp_column].min():.1f}°C, Max: {df[temp_column].max():.1f}°C, Mean: {df[temp_column].mean():.1f}°C")
            
        except FileNotFoundError:
            print(f"Error: File '{csv_file}' not found.")
            continue
        except Exception as e:
            print(f"Error processing {csv_file}: {e}")
            continue
    
    plt.title('Ambient Temperature Monitoring', fontsize=16, fontweight='bold')
    plt.xlabel('Time (per 10 minutes)', fontsize=12)
    plt.ylabel('Temperature (°C)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(loc='upper left', fontsize=10)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(byminute=[0, 30]))
    plt.xticks(rotation=45)
    

    
    plt.tight_layout()
    plt.show()
    
    print("\n=== COMBINED DATA SUMMARY ===")
    if all_temps:
        print(f"Overall temperature range: {min(all_temps):.1f} - {max(all_temps):.1f}°C")
        print(f"Total data points: {len(all_temps)}")

if __name__ == "__main__":
    csv_files = [
        'ambient_temperature_bedroom.csv',
        'ambient_temperature_dining.csv', 
        'ambient_temperature_kitchen.csv',
        'ambient_temperature_lounge.csv'
    ]
    
    room_names = [
        'Bedroom',
        'Dining',
        'Kitchen', 
        'Lounge'
    ]
    
    colors = [
        'red',
        'purple',
        'green',
        'black'
    ]
    
    plot_combined_temperature_data(csv_files, room_names, colors)