# HIT137 Assignment 2 - Question 2 Weather Report Assignment
# Group Name: DAN/EXT 58
# PRADIKSHYA DHAKAL - s396200
# SHEREENA FERNANDO FERNANDO - s387227
# MEL HA - s253796

import pandas as pd
import glob
import os

#mapping months according to the seasons of australia
SEASONS = {
    'Summer': ['December', 'January', 'February'],
    'Autumn': ['March', 'April', 'May'],
    'Winter': ['June', 'July', 'August'],
    'Spring': ['September', 'October', 'November']
}

#CSV files provided by the lecturer loading
def load_all_data(folder="temperatures"):
    files = glob.glob(os.path.join(folder, "*.csv"))
    dataframes = [pd.read_csv(f) for f in files]
    return pd.concat(dataframes, ignore_index=True)

#calculation of the seasonal average for the average temperature
def calculate_seasonal_average(df):
    results = {}
    for season, months in SEASONS.items():
        values = df[months].values.flatten()
        values = pd.Series(values).dropna()
        results[season] = values.mean()
    with open("average_temp.txt", "w") as f:
        for season, avg in results.items():
            f.write(f"{season}: {avg:.1f}°C\n")

#finding the temperature ranges
def find_largest_temp_range(df):
    station_ranges = {}
    for _, row in df.iterrows():
        temps = row[['January','February','March','April','May','June','July',
                     'August','September','October','November','December']]
        temps = temps.dropna()
        if len(temps) == 0:
            continue

        #highest and lowest temperatures calculations
        max_temp = temps.max()
        min_temp = temps.min()
        station_ranges[row['STATION_NAME']] = (max_temp - min_temp, max_temp, min_temp)
    
    if not station_ranges:
        return
    max_range = max(v[0] for v in station_ranges.values())
    with open("largest_temp_range_station.txt", "w") as f:
        for station, (rng, mx, mn) in station_ranges.items():
            if abs(rng - max_range) < 1e-6:
                f.write(f"{station}: Range {rng:.1f}°C (Max: {mx:.1f}°C, Min: {mn:.1f}°C)\n")

#finding stable temperatures
def find_temperature_stability(df):
    station_std = {}
    for _, row in df.iterrows():
        temps = row[['January','February','March','April','May','June','July',
                     'August','September','October','November','December']]
        temps = temps.dropna()
        if len(temps) == 0:
            continue
        station_std[row['STATION_NAME']] = temps.std()
    if not station_std:
        return
    min_std = min(station_std.values())
    max_std = max(station_std.values())

    #to save results in the txt file
    with open("temperature_stability_stations.txt", "w") as f:
        for station, std in station_std.items():
            if abs(std - min_std) < 1e-6:
                f.write(f"Most Stable: {station}: StdDev {std:.1f}°C\n")
        for station, std in station_std.items():
            if abs(std - max_std) < 1e-6:
                f.write(f"Most Variable: {station}: StdDev {std:.1f}°C\n")

#main functions and running the program finally
def main():
    df = load_all_data("temperatures")
    calculate_seasonal_average(df)
    find_largest_temp_range(df)
    find_temperature_stability(df)

if __name__ == "__main__":
    main()
