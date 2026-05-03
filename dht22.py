import time
import socket
import requests
import seeed_dht

API_URL = "https://sensor-api.kentaiwami.com"
API_KEY = "YOUR_API_KEY"
SENSOR_ID = socket.gethostname()
INTERVAL = 15  # seconds

sensor = seeed_dht.DHT("22", 4)

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
    humi, temp = sensor.read()
    if humi is not None:
        print(f"temp={temp:.1f} humi={humi:.1f}")
        post("temperature", round(temp, 2))
        post("humidity", round(humi, 2))
    time.sleep(INTERVAL)
