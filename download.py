import os
import sys
import requests
import subprocess
from datetime import datetime
import re

# Check for command-line arguments
if len(sys.argv) != 3:
    print("Usage: python3 download.py <url> <output_file_base_name>")
    sys.exit(1)

# Get the base URL and output file base name from command-line arguments
BASE_URL = sys.argv[1]
if not re.search(r"seg-\d+", BASE_URL):
    print("Error: URL does not contain a segment identifier (e.g., seg-146).")
    sys.exit(1)

# Replace the hardcoded segment number with a placeholder
BASE_URL = re.sub(r"seg-\d+", "seg-{segment}", BASE_URL)
OUTPUT_BASE_NAME = sys.argv[2]

# Generate a short unique identifier (based on the current time)
unique_id = datetime.now().strftime("%H%M%S")

# Output directory for segments
OUTPUT_DIR = f"video_segments_{unique_id}"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Start downloading segments
segment_number = 1  # Start from segment 1

while True:
    segment_url = BASE_URL.format(segment=segment_number)
    output_file = os.path.join(OUTPUT_DIR, f"seg-{segment_number}.ts")
    print(f"Downloading: {segment_url} -> {output_file}")

    response = requests.get(segment_url, stream=True)

    if response.status_code == 200:
        # Save the segment
        with open(output

