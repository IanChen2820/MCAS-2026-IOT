import time
import board
import adafruit_dht

STUDENT_ID = "N97141467"
DHT_PIN = board.D4  # BCM GPIO4 = physical pin 7
READ_INTERVAL = 2.0  # seconds

sensor = adafruit_dht.DHT11(DHT_PIN, use_pulseio=False)

print(f"Student ID: {STUDENT_ID}")
print("DHT11 temperature and humidity monitor")
print("Press Ctrl+C to stop.")

try:
    while True:
        try:
            temperature_c = sensor.temperature
            humidity = sensor.humidity

            if temperature_c is not None and humidity is not None:
                temperature_f = temperature_c * 9 / 5 + 32
                print(
                    f"{STUDENT_ID} | "
                    f"Temp: {temperature_c:.1f} C / {temperature_f:.1f} F | "
                    f"Humidity: {humidity:.1f}%",
                    flush=True,
                )
            else:
                print(f"{STUDENT_ID} | No valid reading. Try again.", flush=True)

        except RuntimeError as error:
            print(f"{STUDENT_ID} | Read error: {error}", flush=True)

        except Exception as error:
            print(f"{STUDENT_ID} | Sensor error: {error}", flush=True)
            sensor.exit()
            time.sleep(READ_INTERVAL)
            sensor = adafruit_dht.DHT11(DHT_PIN, use_pulseio=False)

        time.sleep(READ_INTERVAL)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")

finally:
    sensor.exit()