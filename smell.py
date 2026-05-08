import sys, smbus, time, socket, requests, datetime

API_URL = "https://sensor-api.kentaiwami.com"
API_KEY = "YOUR_API_KEY"
SENSOR_ID = socket.gethostname()
INTERVAL = 5  # seconds

i2c = smbus.SMBus(1)
addr = 0x68
Vref = 2.048

def swap16(x):
    return (((x << 8) & 0xFF00) | ((x >> 8) & 0x00FF))

def sign16(x):
    return (-(x & 0b1000000000000000) | (x & 0b0111111111111111))

def read_volts():
    i2c.write_byte(addr, 0b10011000)
    time.sleep(0.2)
    data = i2c.read_word_data(addr, 0x00)
    raw = swap16(int(hex(data), 16))
    raw_s = sign16(int(hex(raw), 16))
    return round(Vref * raw_s / 32767, 5)

def post(value):
    try:
        requests.post(
            f"{API_URL}/smell",
            json={"sensor_id": SENSOR_ID, "value": value},
            headers={"X-API-Key": API_KEY},
            timeout=10,
        )
    except Exception as e:
        print(f"error: {e}")

while True:
    volts = read_volts()
    print(f"{datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')} smell={volts}")
    post(volts)
    sys.stdout.flush()
    time.sleep(INTERVAL - 0.2)
