#!/usr/bin/env python3
import pandas as pd
import glob
import time

def naive_read():
    """Read all CSV files using pd.concat() and measure time."""
    print("Starting naive read...")
    start_time = time.perf_counter()
    
    # Get all CSV files
    file_pattern = "generated_small_csvs/*.csv"
    csv_files = glob.glob(file_pattern)
    print(f"Found {len(csv_files)} CSV files")
    
    # Define column names
    column_names = ["id", "timestamp", "items", "category"]
    
    # Read all files and concatenate
    dataframes = []
    for file in csv_files:
        df = pd.read_csv(file, header=None, names=column_names)
        dataframes.append(df)
    
    # Concatenate all dataframes
    df = pd.concat(dataframes, ignore_index=True)
    
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    
    # Print results
    print(f"\nDataFrame head:")
    print(df.head())
    print(f"\nNumber of rows: {len(df)}")
    print(f"Execution time: {execution_time:.2f} seconds")
    
    return df, execution_time

if __name__ == "__main__":
    df, time_taken = naive_read()
