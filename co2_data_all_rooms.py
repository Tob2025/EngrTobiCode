import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

def plot_combined_co2_data(csv_files, room_names, colors, time_column='time', co2_column='co2_ppm', rate_column='rate_of_change'):
    
    plt.figure(figsize=(14, 8))
    
    for i, (csv_file, room_name, color) in enumerate(zip(csv_files, room_names, colors)):
        try:
            df = pd.read_csv(csv_file)
            print(f"Successfully loaded data from {csv_file}")
            print(f"Data shape: {df.shape}")
            
            df['datetime'] = pd.to_datetime('2024-01-01 ' + df[time_column].astype(str))
            df[co2_column] = pd.to_numeric(df[co2_column], errors='coerce')
            
            plt.plot(df['datetime'], df[co2_column], 
                    color=color, linewidth=2, marker='o', markersize=2, 
                    label=f'{room_name}', alpha=0.8)
            
            print(f"{room_name} CO2 - Min: {df[co2_column].min():.0f} ppm, Max: {df[co2_column].max():.0f} ppm, Mean: {df[co2_column].mean():.0f} ppm")
            
        except FileNotFoundError:
            print(f"Error: File '{csv_file}' not found.")
            continue
        except Exception as e:
            print(f"Error processing {csv_file}: {e}")
            continue
    
    plt.title('CO2 Levels Monitoring', fontsize=16, fontweight='bold')
    plt.xlabel('Time (per 10 minutes)', fontsize=12)
    plt.ylabel('CO2 (ppm)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(loc='upper left', fontsize=10)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(byminute=[0, 30]))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    plt.figure(figsize=(14, 8))
    
    for i, (csv_file, room_name, color) in enumerate(zip(csv_files, room_names, colors)):
        try:
            df = pd.read_csv(csv_file)
            
            df['datetime'] = pd.to_datetime('2024-01-01 ' + df[time_column].astype(str))
            df[rate_column] = pd.to_numeric(df[rate_column], errors='coerce').fillna(0)
            
            plt.plot(df['datetime'], df[rate_column], 
                    color=color, linewidth=2, marker='o', markersize=2, 
                    label=f'{room_name}', alpha=0.8)
            
            print(f"{room_name} Rate - Min: {df[rate_column].min():.0f}, Max: {df[rate_column].max():.0f}, Mean: {df[rate_column].mean():.1f}")
            
        except FileNotFoundError:
            print(f"Error: File '{csv_file}' not found.")
            continue
        except Exception as e:
            print(f"Error processing {csv_file}: {e}")
            continue
    
    plt.title('CO2 Rate of Change Monitoring', fontsize=16, fontweight='bold')
    plt.xlabel('Time (per 10 minutes)', fontsize=12)
    plt.ylabel('Rate of Change (ppm/10min)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(loc='upper left', fontsize=10)
    
    plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(byminute=[0, 30]))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    csv_files = [
        'co2_data_bedroom.csv',
        'co2_data_dining.csv', 
        'co2_data_kitchen.csv',
        'co2_data_lounge.csv'
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
    
    plot_combined_co2_data(csv_files, room_names, colors)