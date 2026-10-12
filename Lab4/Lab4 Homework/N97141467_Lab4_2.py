from gpiozero import DistanceSensor
from time import sleep

STUDENT_ID = "N97141467"
TRIG = 23  # BCM GPIO23 = physical pin 16
ECHO = 24  # BCM GPIO24 = physical pin 18
WARNING_DISTANCE = 20  # cm

sensor = DistanceSensor(echo=ECHO, trigger=TRIG, max_distance=4)

print(f"Student ID: {STUDENT_ID}")
print("Parking sensor simulation")
print("Press Ctrl+C to stop.")

try:
    while True:
        distance_cm = sensor.distance * 100

        print(f"{STUDENT_ID} | 目前距離: {distance_cm:.2f} cm", flush=True)

        if distance_cm < WARNING_DISTANCE:
            print(f"{STUDENT_ID} | 注意！！！", flush=True)
        else:
            print(f"{STUDENT_ID} | 沒事", flush=True)

        sleep(0.5)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")

finally:
    sensor.close()
