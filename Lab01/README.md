# Data Engineering Lab - Simple Join

This lab demonstrates performance differences in reading and processing CSV data using different approaches.

## Setup

The project uses `uv` for Python environment management and includes the following dependencies:
- pandas
- tqdm
- faker

Additional tools used:
- GNU Parallel (for file merging)
- hyperfine (for performance benchmarking)

## Files Generated

- `generated_small_csvs/` - Directory with 50,000 CSV files (~1GB total)
- `transactions.csv` - Merged CSV file (~976MB)
- `transactions.csv.gz` - Compressed version (~209MB)

## Scripts

### Data Generation
- `generate_data.py` - Generates test dataset with 50,000 CSV files

### Performance Tests
- `03_naive_read.py` - Reads all files individually using pd.concat()
- `04_single_file_read.py` - Reads the merged CSV file
- `05_three_options.py` - Compares three different data processing functions
- `summary.py` - Provides detailed analysis and explanations
- `benchmark.sh` - Runs performance tests using hyperfine

## Results Summary

### Reading Performance
1. **Naive Read (50k files)**: ~26.69 seconds
2. **Single File Read**: ~7.58 seconds (3.5x faster)

### Function Comparison (on gzipped data)
1. **Function 1 (pandas)**: 9.47 seconds
2. **Function 2 (csv.DictReader)**: 10.57 seconds  
3. **Function 3 (raw processing)**: 4.21 seconds (fastest)

## Key Insights

- **File I/O overhead**: Opening many small files is much slower than reading one large file
- **Processing approaches**: Raw string processing can be 2x faster than pandas for filtered queries
- **Compression**: Gzip reduces file size by ~80% (976MB → 209MB)
- **Trade-offs**: Faster methods may sacrifice robustness and error handling

## Running the Lab

```bash
# Generate data
uv run python generate_data.py

# Test naive approach  
uv run python 03_naive_read.py

# Merge files using GNU Parallel
cd generated_small_csvs && find . -name "*.csv" | parallel -j 8 "cat {}" > ../transactions.csv

# Test single file approach
uv run python 04_single_file_read.py

# Compare three functions
uv run python 05_three_options.py

# View detailed analysis
uv run python summary.py

# Run benchmarks (optional)
./benchmark.sh
```

## Lessons Learned

1. **Minimize file operations** - Consolidate small files before processing
2. **Choose appropriate tools** - Raw processing for known formats, pandas for complex analysis
3. **Consider compression** - Significant storage savings with minimal performance impact
4. **Profile before optimizing** - Measure actual performance rather than assuming bottlenecks
