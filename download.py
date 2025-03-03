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
failed_segments = []

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

# Check if any segments were downloaded
if segment_number == 1:
    print("No segments downloaded. Exiting...")
    sys.exit(1)

# Merge downloaded segments into a single file
output_video_ts = f"{output_base_name}.ts"
print("Merging segments into a single .ts file...")

try:
    with open(output_video_ts, "wb") as outfile:
        for num in range(1, segment_number):
            segment_file = os.path.join(output_dir, f"seg-{num}.ts")
            if os.path.exists(segment_file):
                with open(segment_file, "rb") as infile:
                    outfile.write(infile.read())
            else:
                failed_segments.append(segment_file)
except Exception as e:
    print(f"Error during merging: {e}")
    sys.exit(1)

# Log any failed segments
if failed_segments:
    with open("failed_segments.log", "w") as log:
        log.write("\n".join(failed_segments))
    print(f"Failed segments logged to failed_segments.log")

# Convert merged .ts file to .mp4
output_video_mp4 = f"{output_base_name}.mp4"
if os.path.exists(output_video_ts):
    print("Converting .ts file to .mp4...")
    try:
        subprocess.run(["ffmpeg", "-i", output_video_ts, "-c", "copy", output_video_mp4], check=True)
        print(f"Download, merge, and conversion complete. Output file: {output_video_mp4}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)
else:
    print("Error: .ts file not found, conversion to .mp4 skipped.")

