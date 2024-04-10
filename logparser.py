import sys
import glob
import csv
import re

# Define the strings to search for in the log files
strings_to_search = [
    "register connected",
    "register success",
    "registered",
    "call incoming",
    "call started",
    "call connected",
]

# Initialize a dictionary to count the occurrences of each string
string_counts = {string: 0 for string in strings_to_search}

# Check if log file patterns are provided as command-line arguments
if len(sys.argv) < 2:
    print("Usage: python log_parser.py <log_file_pattern> [<log_file_pattern> ...]")
    sys.exit(1)

# Collect all log files based on the provided patterns
log_files = []
for pattern in sys.argv[1:]:
    log_files.extend(glob.glob(pattern))

# Create a CSV file to write the data
csv_file = "log_data.csv"

with open(csv_file, mode="w", newline="") as csv_file:
    fieldnames = ["MSIDN", "String Searched", "Time of Event", "Error", "File Name"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Process each log file
    for log_file in log_files:
        try:
            # Determine the file type (listener, talker, or other)
            if "listener" in log_file:
                file_type = "listener"
            elif "talker" in log_file:
                file_type = "talker"
            else:
                file_type = "other"

            # Open and read the log file
            with open(log_file, "r") as file:
                for line in file:
                    # Check if any of the strings are present in the line
                    for string in strings_to_search:
                        if string in line:
                            # Extract MSIDN from the line
                            msidn_match = re.search(r"'(\d+)'", line)
                            msidn = msidn_match.group(1) if msidn_match else "N/A"

                            # Get the time of the event
                            time_match = re.search(r"(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}.\d{3})", line)
                            event_time = time_match.group(1) if time_match else "N/A"

                            # Increment the count for the matched string
                            string_counts[string] += 1

                            # Write the data to the CSV file
                            writer.writerow({
                                "MSIDN": msidn,
                                "String Searched": string,
                                "Time of Event": event_time,
                                "Error": "N/A",  # Set to "N/A" for non-error entries
                                "File Name": log_file
                            })

                        elif '"error":"' in line:
                            # Extract MSIDN from the line
                            msidn_match = re.search(r"'(\d+)'", line)
                            msidn = msidn_match.group(1) if msidn_match else "N/A"

                            # Get the time of the event
                            time_match = re.search(r"(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}.\d{3})", line)
                            event_time = time_match.group(1) if time_match else "N/A"

                            # Extract the "error" field if it exists
                            error_match = re.search(r'"error":"(.*?)"', line)
                            error = error_match.group(1) if error_match else "N/A"

                            # Write the data to the CSV file
                            writer.writerow({
                                "MSIDN": msidn,
                                "String Searched": "error",
                                "Time of Event": event_time,
                                "Error": error,
                                "File Name": log_file
                            })

        except FileNotFoundError:
            print(f"Error: File '{log_file}' not found.")
            continue

# Print the counts for each string
for string, count in string_counts.items():
    print(f"{string}: {count}")

print(f"Data has been written to {csv_file}")
