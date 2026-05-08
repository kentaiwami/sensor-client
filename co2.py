import time
import socket
import requests
import mh_z19

API_URL = "https://sensor-api.kentaiwami.com"
API_KEY = "YOUR_API_KEY"
SENSOR_ID = socket.gethostname()
INTERVAL = 15  # seconds

def post(endpoint, value):
    try:
        requests.post(
            f"{API_URL}/{endpoint}",
            json={"sensor_id": SENSOR_ID, "value": value},
            headers={"X-API-Key": API_KEY},
            timeout=10,
        )
    except Exception as e:
        print(f"error: {e}")

while True:
    data = mh_z19.read_all()
    co2 = data.get("co2")
    if co2 is not None:
        print(f"co2={co2}")
        post("co2", co2)
    time.sleep(INTERVAL)
