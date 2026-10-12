import time
import serial
from gpiozero import LED

STUDENT_ID = "N97141467"
LED_PIN = 17  # BCM GPIO17 = physical pin 11
PORT = "/dev/serial0"
BAUD = 9600

led = LED(LED_PIN)
ser = serial.Serial(PORT, BAUD, timeout=1)

def blink(times):
    for _ in range(times):
        led.on()
        time.sleep(0.3)
        led.off()
        time.sleep(0.3)

print(f"Student ID: {STUDENT_ID}")
print("UART loopback: type a digit 1-9, LED blinks that many times.")
print("Type q to quit.")

try:
    while True:
        text = input("Send (1-9 / q): ").strip()

        if text.lower() == "q":
            break

        if len(text) != 1 or not text.isdigit() or text == "0":
            print("Please enter one digit from 1 to 9.")
            continue

        ser.reset_input_buffer()
        ser.write(text.encode())
        print(f"{STUDENT_ID} | Sent: {text}", flush=True)

        received = ser.read(1).decode(errors="ignore")

        if received == "":
            print(f"{STUDENT_ID} | Received: nothing. Check TX/RX wire.", flush=True)
            continue

        print(f"{STUDENT_ID} | Received: {received}", flush=True)
        blink(int(received))

except KeyboardInterrupt:
    print("\nStopped.")

finally:
    ser.close()
    led.close()
