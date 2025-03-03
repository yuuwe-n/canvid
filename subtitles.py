import re
import sys
import pyperclip
from bs4 import BeautifulSoup

def extract_subtitles_from_html(html_content):
    """Extract subtitles and timestamps from HTML and generate SRT content."""
    soup = BeautifulSoup(html_content, "html.parser")
    subtitle_entries = []

    # Extract spans with time data
    for idx, span in enumerate(soup.find_all("span", class_="transcription-time-part"), start=1):
        start_time = float(span["data-time-start"])
        end_time = float(span["data-time-end"])
        text = span.get_text(strip=True)

        # Convert seconds to HH:MM:SS,ms format
        start_timestamp = seconds_to_timestamp(start_time)
        end_timestamp = seconds_to_timestamp(end_time)

        # Create an SRT entry
        subtitle_entries.append(f"{idx}\n{start_timestamp} --> {end_timestamp}\n{text}\n")

    return "\n".join(subtitle_entries)

def seconds_to_timestamp(seconds):
    """Convert seconds to HH:MM:SS,ms format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

def write_to_file(content, output_path):
    """Write content to a file."""
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(content)

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_srt.py <output_srt>")
        sys.exit(1)

    output_srt = sys.argv[1]

    # Get clipboard content
    clipboard_content = pyperclip.paste()

    if not clipboard_content.strip():
        print("Clipboard is empty. Please copy the HTML content first.")
        sys.exit(1)

    # Save clipboard content to subtitles.html
    html_file = "subtitles.html"
    write_to_file(clipboard_content, html_file)

    # Extract subtitles and save to SRT file
    srt_content = extract_subtitles_from_html(clipboard_content)
    write_to_file(srt_content, output_srt)

    print(f"SRT file created successfully: {output_srt}")

if __name__ == "__main__":
    main()
