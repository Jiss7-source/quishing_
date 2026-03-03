import pandas as pd
import os

# Check what files are in your dataset folder
print("Files in dataset folder:")
print(os.listdir("dataset"))

# Load and inspect — adjust the filename to match what you downloaded
# Try each one until it works
for filename in os.listdir("dataset"):
    if filename.endswith(".csv"):
        print(f"\n--- Inspecting: {filename} ---")
        try:
            df = pd.read_csv(f"dataset/{filename}", nrows=5)
            print("Columns:", df.columns.tolist())
            print("Shape:", df.shape)
            print("First 3 rows:")
            print(df.head(3))
        except Exception as e:
            print(f"Could not read {filename}: {e}")