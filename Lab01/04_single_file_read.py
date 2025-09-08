#!/usr/bin/env python3
import pandas as pd
import time

def read_single_file():
    """Read the merged CSV file and measure time."""
    print("Starting single file read...")
    start_time = time.perf_counter()
    
    # Define column names
    column_names = ["id", "timestamp", "items", "category"]
    
    # Read the merged file
    df = pd.read_csv("transactions.csv", header=None, names=column_names)
    
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    
    # Print results
    print(f"\nDataFrame head:")
    print(df.head())
    print(f"\nNumber of rows: {len(df)}")
    print(f"Execution time: {execution_time:.2f} seconds")
    
    return df, execution_time

if __name__ == "__main__":
    df, time_taken = read_single_file()
