#!/usr/bin/env python3
import pandas as pd
import time
import random
import csv
import gzip
import io

def read_and_sample():
    """Read the merged CSV file and print 10 random rows with most common category."""
    print("Reading single file and sampling...")
    
    # Define column names
    column_names = ["id", "timestamp", "items", "category"]
    
    # Read the merged file
    df = pd.read_csv("transactions.csv", header=None, names=column_names)
    
    # Sample 10 random rows
    random_sample = df.sample(n=10, random_state=42)
    print(f"\n10 random rows:")
    print(random_sample)
    
    # Find most common category among these 10 rows
    most_common_category = random_sample['category'].mode()[0]
    print(f"\nMost common category among these 10 rows: {most_common_category}")
    
    return df, random_sample, most_common_category

# Function 1: Using pandas
def get_csv_data_pandas(filename, category, idset):
    names = ["id", "timestamp", "items", "category"]
    df = pd.read_csv(filename, header=None, names=names)
    return df[(df["id"].isin(idset)) & (df["category"] == category)].to_dict("records")

# Function 2: Using csv module with gzip
def get_csv_data_raw(filename, category, idset):
    names = ["id", "timestamp", "items", "category"]
    data = []
    with gzip.open(filename, "rt") as r_file:
        f = csv.DictReader(r_file, names)
        for line in f:
            if int(line["id"]) in idset and line["category"] == category:
                line["id"] = int(line["id"])
                data.append(line)
    return data

# Function 3: Raw string processing with gzip
def get_csv_data_raw2(filename, category, idset):
    names = ["id", "timestamp", "items", "category"]
    data = []
    with gzip.open(filename, "rb") as r_file:
        for line in r_file:
            decoded = line.decode("utf-8").rstrip("\n")
            if category in decoded:
                parts = decoded.split(',"')
                if int(parts[0]) in idset:
                    data.append(
                        {
                            f: int(val) if f == "id" else val.strip('"')
                            for f, val in zip(names, parts)
                        }
                    )
    return data

def test_functions():
    """Test and compare the three functions."""
    print("\n" + "="*60)
    print("TESTING THE THREE FUNCTIONS")
    print("="*60)
    
    # First, create a gzipped version of our CSV for testing
    print("Creating gzipped version of transactions.csv...")
    with open("transactions.csv", "rb") as f_in:
        with gzip.open("transactions.csv.gz", "wb") as f_out:
            f_out.writelines(f_in)
    
    # Test parameters
    category = "Toys"
    idset = {1894763, 5764159, 8933236, 2728762, 3360477}  # Some IDs from our sample
    filename = "transactions.csv.gz"
    
    print(f"Testing with category: {category}")
    print(f"Testing with ID set: {idset}")
    
    # Test Function 1
    print(f"\nTesting Function 1 (pandas)...")
    start_time = time.perf_counter()
    result1 = get_csv_data_pandas(filename, category, idset)
    end_time = time.perf_counter()
    time1 = end_time - start_time
    print(f"Function 1 time: {time1:.4f} seconds")
    print(f"Function 1 results: {len(result1)} records")
    
    # Test Function 2  
    print(f"\nTesting Function 2 (csv.DictReader)...")
    start_time = time.perf_counter()
    result2 = get_csv_data_raw(filename, category, idset)
    end_time = time.perf_counter()
    time2 = end_time - start_time
    print(f"Function 2 time: {time2:.4f} seconds")
    print(f"Function 2 results: {len(result2)} records")
    
    # Test Function 3
    print(f"\nTesting Function 3 (raw string processing)...")
    start_time = time.perf_counter()
    result3 = get_csv_data_raw2(filename, category, idset)
    end_time = time.perf_counter()
    time3 = end_time - start_time
    print(f"Function 3 time: {time3:.4f} seconds")
    print(f"Function 3 results: {len(result3)} records")
    
    # Verify results are the same
    print(f"\n" + "-"*40)
    print("VERIFICATION")
    print("-"*40)
    
    # Sort results by ID for comparison
    result1_sorted = sorted(result1, key=lambda x: x['id'])
    result2_sorted = sorted(result2, key=lambda x: x['id'])
    result3_sorted = sorted(result3, key=lambda x: x['id'])
    
    print(f"Results lengths match: {len(result1_sorted) == len(result2_sorted) == len(result3_sorted)}")
    
    # Compare first few results
    if result1_sorted and result2_sorted and result3_sorted:
        print(f"First result from Function 1: {result1_sorted[0]}")
        print(f"First result from Function 2: {result2_sorted[0]}")
        print(f"First result from Function 3: {result3_sorted[0]}")
        
        # Check if all IDs match
        ids1 = {r['id'] for r in result1_sorted}
        ids2 = {r['id'] for r in result2_sorted}
        ids3 = {r['id'] for r in result3_sorted}
        print(f"All IDs match: {ids1 == ids2 == ids3}")
    
    # Performance summary
    print(f"\n" + "-"*40)
    print("PERFORMANCE SUMMARY")
    print("-"*40)
    print(f"Function 1 (pandas):           {time1:.4f} seconds")
    print(f"Function 2 (csv.DictReader):   {time2:.4f} seconds")
    print(f"Function 3 (raw processing):   {time3:.4f} seconds")
    
    # Calculate relative performance
    times = [time1, time2, time3]
    fastest = min(times)
    print(f"\nRelative performance (fastest = 1.0x):")
    print(f"Function 1: {time1/fastest:.2f}x")
    print(f"Function 2: {time2/fastest:.2f}x")
    print(f"Function 3: {time3/fastest:.2f}x")

if __name__ == "__main__":
    df, sample, common_cat = read_and_sample()
    test_functions()
