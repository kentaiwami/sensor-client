import asyncio
import requests
from bleak import BleakScanner

TILE_UUID = "YOUR_TILE_UUID"
API_URL = "https://sensor-api.kentaiwami.com"
API_KEY = "YOUR_API_KEY"
LOCATION = "work_room"
INTERVAL = 0  # seconds

def post(rssi):
    try:
        requests.post(
            f"{API_URL}/ble/rssi",
            json={"location": LOCATION, "rssi": rssi},
            headers={"X-API-Key": API_KEY},
            timeout=10,
        )
    except Exception as e:
        print(f"error: {e}")

async def main():
    while True:
        results = await BleakScanner.discover(timeout=5.0, return_adv=True)
        found = [(d, adv) for d, adv in results.values() if TILE_UUID in adv.service_uuids]
        if found:
            _, adv = found[0]
            print(f"RSSI: {adv.rssi} dBm  location: {LOCATION}")
            post(adv.rssi)
        else:
            print("not detected")
        await asyncio.sleep(INTERVAL)

asyncio.run(main())
