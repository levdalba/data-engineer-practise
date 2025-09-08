#!/usr/bin/env python3
import os
import math
import random
import pathlib
from faker import Faker
from datetime import datetime
from tqdm import tqdm  # progress bar

# ------------ Config ------------
OUT_DIR = pathlib.Path("generated_small_csvs")
NUM_FILES = 50_000
TARGET_TOTAL_BYTES = 1_000_000_000  # ~1 GB on disk
SEED = 42  # set to None for non-deterministic
MIN_ITEMS_PER_ROW = 1
MAX_ITEMS_PER_ROW = 12
MAX_ID = 10000000
# --------------------------------

if SEED is not None:
    random.seed(SEED)

fake = Faker("en_US")
if SEED is not None:
    Faker.seed(SEED)

# Categories
CATEGORIES = ["Food", "Toys", "Electronics", "Books", "Stationery", "Tools"]

# Balanced items across categories
ITEMS_BY_CATEGORY = {
    "Food": [
        "whole milk", "yogurt", "cream cheese", "bottled water", "soda",
        "tropical fruit", "citrus fruit", "berries", "semi-finished bread",
        "rolls/buns", "chocolate", "bottled beer",
    ],
    "Toys": [
        "building blocks", "action figure", "doll", "puzzle", "board game",
        "toy car", "plush bear", "yo-yo", "kite", "water gun", "RC drone", "slime",
    ],
    "Electronics": [
        "battery AA", "battery AAA", "USB cable", "HDMI cable", "phone charger",
        "power bank", "headphones", "bluetooth speaker", "LED bulb",
        "extension cord", "wireless mouse", "keyboard",
    ],
    "Books": [
        "novel", "textbook", "children book", "cookbook", "travel guide",
        "mystery novel", "sci-fi novel", "fantasy novel", "comic book",
        "workbook", "dictionary", "magazine",
    ],
    "Stationery": [
        "paper clips", "notebook", "gel pen", "highlighter", "stapler",
        "sticky notes", "binder", "eraser", "pencil", "marker",
        "correction tape", "ruler",
    ],
    "Tools": [
        "hammer", "screwdriver", "wrench", "drill bits", "pliers",
        "tape measure", "utility knife", "level", "sandpaper",
        "nails", "screws", "toolbox",
    ],
}

def rand_timestamp() -> str:
    dt = fake.date_time_between(datetime(2010, 1, 1), datetime(2020, 1, 1))
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def rand_category() -> str:
    return random.choice(CATEGORIES)

def rand_items_for_category(category: str) -> str:
    pool = ITEMS_BY_CATEGORY[category]
    k = random.randint(MIN_ITEMS_PER_ROW, min(MAX_ITEMS_PER_ROW, len(pool)))
    return ",".join(random.sample(pool, k))

def make_row(id5: str) -> str:
    ts = rand_timestamp()
    cat = rand_category()
    items = rand_items_for_category(cat)
    return f'{id5},"{ts}","{items}","{cat}"\n'

# --- Estimate rows ---
SAMPLE_N = 1000
sample_bytes = sum(len(make_row(f"{i:05d}").encode("utf-8")) for i in range(SAMPLE_N))
avg_bytes_per_row = sample_bytes / SAMPLE_N

total_rows_needed = math.ceil(TARGET_TOTAL_BYTES / avg_bytes_per_row)
if total_rows_needed > MAX_ID:
    raise SystemExit(
        f"Requested ~{total_rows_needed} rows, but only {MAX_ID} unique IDs possible. "
        f"Either lower TARGET_TOTAL_BYTES or allow duplicate IDs."
    )

rows_per_file = max(1, total_rows_needed // NUM_FILES)
remainder_rows = total_rows_needed - (rows_per_file * NUM_FILES)

OUT_DIR.mkdir(parents=True, exist_ok=True)
if list(OUT_DIR.glob("part_*.csv")):
    raise SystemExit(f"Output directory {OUT_DIR} is not empty. Clear it first.")

print(f"Estimated avg bytes/row: {avg_bytes_per_row:.1f}")
print(f"Target total bytes:      {TARGET_TOTAL_BYTES:,}")
print(f"Total rows needed:       {total_rows_needed:,}")
print(f"Rows per file (base):    {rows_per_file}")
print(f"Files with +1 row:       {remainder_rows}")

# --- Prepare unique IDs ---
print("Preparing unique IDs...")
ids = [f"{i:0{len(str(MAX_ID))-1}d}" for i in range(MAX_ID)]
random.shuffle(ids)
ids = ids[:total_rows_needed]
id_iter = iter(ids)
print("IDs generated")

# --- Generate files with tqdm ---
cumulative_bytes = 0
for i in tqdm(range(1, NUM_FILES + 1), desc="Generating CSV files", unit="file"):
    n_rows = rows_per_file + (1 if i <= remainder_rows else 0)
    fname = OUT_DIR / f"part_{i:06d}.csv"
    with open(fname, "wb") as f:
        for _ in range(n_rows):
            f.write(make_row(next(id_iter)).encode("utf-8"))
    cumulative_bytes += fname.stat().st_size

print("\nDone.")
print(f"Final size: {cumulative_bytes/1_000_000:.1f} MB")

