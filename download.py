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
original_url = sys.argv[1]
if not re.search(r"seg-\d+", original_url):
    print("Error: URL does not contain a segment identifier (e.g., seg-46).")
    sys.exit(1)

# Replace the segment number with a placeholder
base_url = re.sub(r"seg-\d+", "seg-{segment}", original_url)
output_base_name = sys.argv[2]

# Generate a short unique identifier (based on the current time)
unique_id = datetime.now().strftime("%H%M%S")

# Output directory for segments
output_dir = f"video_segments_{unique_id}"
os.makedirs(output_dir, exist_ok=True)

# Start downloading segments
segment_number = 1  # Start from segment 1

while True:
    segment_url = base_url.format(segment=segment_number)
    output_file = os.path.join(output_dir, f"seg-{segment_number}.ts")
    print(f"Downloading: {segment_url} -> {output_file}")

    response = requests.get(segment_url, stream=True)

    if response.status_code == 200:
        # Save the segment
        with open(output_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        print(f"No more segments found or failed to download: {segment_url} (HTTP {response.status_code})")
        break

    segment_number += 1

# Merge downloaded segments into a single file
output_video_ts = f"{output_base_name}.ts"
segment_files = os.path.join(output_dir, "seg-*.ts")

print("Merging segments into a single .ts file...")
subprocess.run(f"cat {segment_files} > {output_video_ts}", shell=True, check=True)

# Convert merged .ts file to .mp4
output_video_mp4 = f"{output_base_name}.mp4"
print("Converting .ts file to .mp4...")
subprocess.run(["ffmpeg", "-i", output_video_ts, "-c", "copy", output_video_mp4], check=True)

print(f"Download, merge, and conversion complete. Output file: {output_video_mp4}")

