#!/bin/bash

echo "PERFORMANCE TESTING WITH HYPERFINE"
echo "=================================="

echo ""
echo "Testing naive read (multiple files)..."
hyperfine --min-runs 3 --max-runs 5 "uv run python 03_naive_read.py"

echo ""
echo "Testing single file read..."
hyperfine --min-runs 3 --max-runs 5 "uv run python 04_single_file_read.py"

echo ""
echo "Testing three functions comparison..."
hyperfine --min-runs 3 --max-runs 5 "uv run python 05_three_options.py"
