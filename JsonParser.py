import json

# Define input and output file paths
input_file = "./log/messages.log"  # Change this to your actual JSON file
output_file = "filtered_messages.json"

# Define keys of interest
TOS_EVENTS = {"gdp", "ground_stop", "reroute", "tmi"}
ROUTE_KEYS = {"routeOfFlight", "trajectory", "flightId"}

filtered_data = []

# Read file line by line
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        try:
            flight = json.loads(line.strip())  # Parse each line as a JSON object
            extracted_info = {}

            # Extract relevant TOS events
            for key in TOS_EVENTS:
                if key in flight:
                    extracted_info[key] = flight[key]

            # Extract relevant route-related data
            for key in ROUTE_KEYS:
                if key in flight:
                    extracted_info[key] = flight[key]

            # Include flight ID if available
            if "acid" in flight:
                extracted_info["acid"] = flight["acid"]

            # Only add if relevant data exists
            if extracted_info:
                filtered_data.append(extracted_info)

        except json.JSONDecodeError:
            print(f"Skipping invalid JSON line: {line.strip()}")

# Save filtered data
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(filtered_data, f, indent=4)

print(f"✅ Extracted {len(filtered_data)} relevant records and saved to {output_file}")