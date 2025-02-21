import json

input_file = "./log/messages.log"  # Replace with your actual file name

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        try:
            raw_data = json.loads(line.strip())  # Load JSON object
            print(json.dumps(raw_data, indent=2))  # Pretty-print full structure
            break  # Stop after printing the first valid JSON object
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            continue
