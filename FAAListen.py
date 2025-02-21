import json
import stomp

# FAA SWIM Connection Details (Modify as Needed)
HOST = "ems1.swim.faa.gov"
PORT = 55443  # From your -DproviderUrl (tcps://ems1.swim.faa.gov:55443)
USER = "jaehan.im.utexas.edu"
PASSWORD = "b9W_99eeSGC_BG-xKI1TYg"
QUEUE = "/queue/jaehan.im.utexas.edu.TFMS.a64dc71f-b217-4803-abd2-c0716760d8ff.OUT"

# Keywords for filtering
TOS_EVENTS = {"gdp", "ground_stop", "reroute", "tmi"}
ROUTE_KEYS = {"routeOfFlight", "trajectory", "flightId"}

class FAAListener(stomp.ConnectionListener):
    """Handles incoming FAA messages in real-time."""
    
    def on_message(self, frame):
        """Processes incoming messages and extracts relevant data."""
        try:
            data = json.loads(frame.body)

            # Filter TOS-related messages
            if "eventType" in data and data["eventType"] in TOS_EVENTS:
                print(f"TOS Event: {data['eventType']} at {data.get('airport', 'Unknown')}")

            # Filter Route-related messages
            elif any(key in data for key in ROUTE_KEYS):
                print(f"Flight {data.get('flightId', 'Unknown')} - Filed Route: {data.get('routeOfFlight', 'N/A')}")
                print(f"Actual Route: {data.get('trajectory', {}).get('fixList', [])}")

        except json.JSONDecodeError:
            print("Received a non-JSON message. Skipping.")

# # Connect to FAA SWIM
conn = stomp.Connection([(HOST, PORT)])
conn.set_listener("", FAAListener())
conn.connect(USER, PASSWORD, wait=True)

# # Subscribe to your queue
conn.subscribe(destination=QUEUE, id=1, ack="auto")

print("Listening for FAA messages...")

# # Keep running
try:
    while True:
        pass
except KeyboardInterrupt:
    conn.disconnect()
    print("Disconnected from FAA SWIM.")
