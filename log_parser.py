import re
import sys
import glob
import pandas as pd
from itertools import repeat
import matplotlib.pyplot as plt

# Define the strings to search for in the log files
strings_to_search = [
    "register connected",
    "register success",
    "registered",
    "call incoming",
    "call started",
    "call connected",
]
timestamp_pattern = r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}'
message_pattern = r'.*\|(.*)'
msidn_pattern = r"10011\d{5}"


# Initialize a dictionary to count the occurrences of each string
string_counts = {string: 0 for string in strings_to_search}

# Check if log file patterns are provided as command-line arguments
if len(sys.argv) < 2:
    print("Usage: python log_parser.py <log_file_pattern> [<log_file_pattern> ...]")
    sys.exit(1)
file_type = sys.argv[1:][0].split("-")[0]
# print(sys.argv[1:][0].split("-")[0])
# Collect all log files based on the provided patterns
log_files = []
for pattern in sys.argv[1:]:
    log_files.extend(glob.glob(pattern))
timestamps = list()
messages = list()
msidns = list()
# Process each log file
for log_file in log_files:
    try:
        # Open and read the log file
        with open(log_file, "r") as file:
            for line in file:
                # print(line)
                timestamps.append(re.match(timestamp_pattern,line).group())
                message = line.split("|")
                messages.append(message[len(message)-1])
                msidn = re.search(msidn_pattern,line)
                msidns.append(msidn.group(0) if msidn else "")
                # if (re.match(msidn_pattern,line)):
                #     msidns.append(re.match(msidn_pattern,line).group())
                # Check if any of the strings are present in the line
                for string in strings_to_search:
                    if string in line:
                        # Increment the count for the matched string
                        string_counts[string] += 1
                # string_counts["type"]= file_type
    except FileNotFoundError:
        print(f"Error: File '{log_file}' not found.")
        continue
# print(len(messages))
# print(len(timestamps))
# print(len(msidns))
# print([s for s in msidns if s])
# print(list(repeat(file_type, len(messages))))
data = {
    "time": timestamps,
    "messages": messages,
    "msidn": msidns,
    "type": list(repeat(file_type, len(messages))),
}
df = pd.DataFrame(data)
df.to_csv("log.csv",index=False)

# print(msidns,len(msidns))
# Print the counts for each string
record = {string:[count] for string, count in string_counts.items()}
df = pd.DataFrame(record)
df.to_csv("record.csv",index=False)
# print(record)
plt.pie(df.iloc[0].values, labels=df.columns, autopct='%1.0f%%', startangle=140)
plt.show()



    