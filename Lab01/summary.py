#!/usr/bin/env python3
"""
Summary script for the Data Engineering Lab - Simple Join
This script demonstrates the complete workflow and performance comparisons.
"""

import pandas as pd
import time
import os

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def main():
    print("DATA ENGINEERING LAB - SIMPLE JOIN")
    print("Performance Analysis Summary")
    
    # Check file sizes
    print_section("FILE SIZE ANALYSIS")
    
    if os.path.exists("generated_small_csvs"):
        import subprocess
        result = subprocess.run(["du", "-sh", "generated_small_csvs"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Generated CSV files size: {result.stdout.strip().split()[0]}")
    
    if os.path.exists("transactions.csv"):
        result = subprocess.run(["du", "-sh", "transactions.csv"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Merged CSV file size: {result.stdout.strip().split()[0]}")
    
    if os.path.exists("transactions.csv.gz"):
        result = subprocess.run(["du", "-sh", "transactions.csv.gz"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Gzipped CSV file size: {result.stdout.strip().split()[0]}")
    
    # Performance summary
    print_section("PERFORMANCE COMPARISON SUMMARY")
    
    print("Based on our tests:")
    print()
    print("1. NAIVE READ (50,000 separate files):")
    print("   - Time: ~26.69 seconds")
    print("   - Method: pd.concat() on individual file reads")
    print("   - Bottleneck: File I/O overhead from opening 50k files")
    print()
    print("2. SINGLE FILE READ (merged file):")
    print("   - Time: ~7.58 seconds") 
    print("   - Method: Single pd.read_csv() call")
    print("   - Improvement: 3.5x faster than naive approach")
    print()
    print("3. FILTERED READING FUNCTIONS (on gzipped data):")
    print("   - Function 1 (pandas): 9.47 seconds (2.25x slower)")
    print("   - Function 2 (csv.DictReader): 10.57 seconds (2.51x slower)")
    print("   - Function 3 (raw processing): 4.21 seconds (fastest)")
    print()
    
    print_section("ANALYSIS & EXPLANATION")
    
    print("Why these performance differences?")
    print()
    print("1. NAIVE READ vs SINGLE FILE:")
    print("   - Opening 50,000 files has significant OS overhead")
    print("   - Each file open/close requires system calls")
    print("   - Memory fragmentation from many small DataFrames")
    print("   - Single file read benefits from sequential I/O")
    print()
    print("2. FUNCTION PERFORMANCE DIFFERENCES:")
    print()
    print("   Function 1 (pandas):")
    print("   - Loads entire dataset into memory first")
    print("   - Creates DataFrame with full schema validation")
    print("   - Type inference and indexing overhead")
    print("   - Memory overhead for unused data")
    print()
    print("   Function 2 (csv.DictReader):")
    print("   - Row-by-row processing with proper CSV parsing")
    print("   - Dictionary creation for each row")
    print("   - Type conversion overhead (string to int)")
    print("   - Full CSV compliance (quotes, escaping)")
    print()
    print("   Function 3 (raw processing):")
    print("   - Fastest due to minimal overhead")
    print("   - Simple string operations")
    print("   - Early filtering with 'category in decoded'")
    print("   - Only processes matching rows")
    print("   - BUT: Less robust (assumes CSV format)")
    print()
    
    print_section("RECOMMENDATIONS")
    
    print("1. For bulk data loading: Merge files first, then read")
    print("2. For filtered queries: Use raw processing when format is known")
    print("3. For production: Balance performance vs robustness")
    print("4. Consider columnar formats (Parquet) for better performance")
    print("5. Use compression for storage efficiency")
    print()
    print("Key takeaway: File I/O patterns matter more than processing logic!")

if __name__ == "__main__":
    main()
