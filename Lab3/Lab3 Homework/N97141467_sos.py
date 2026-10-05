import RPi.GPIO as GPIO
import time

LED_PIN = 11       # LED：實體 Pin 11（GPIO17）
BUZZER_PIN = 13    # 蜂鳴器：實體 Pin 13（GPIO27）

DOT = 0.2
DASH = DOT * 3
SIGNAL_GAP = DOT
LETTER_GAP = DOT * 3
FREQUENCY = 888

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)

buzzer = GPIO.PWM(BUZZER_PIN, FREQUENCY)
buzzer.start(0)

def signal(duration):
    GPIO.output(LED_PIN, GPIO.HIGH)
    buzzer.ChangeDutyCycle(50)
    time.sleep(duration)

    GPIO.output(LED_PIN, GPIO.LOW)
    buzzer.ChangeDutyCycle(0)
    time.sleep(SIGNAL_GAP)

def send_sos():
    # S：3 短
    for _ in range(3):
        signal(DOT)

    time.sleep(LETTER_GAP - SIGNAL_GAP)

    # O：3 長
    for _ in range(3):
        signal(DASH)

    time.sleep(LETTER_GAP - SIGNAL_GAP)

    # S：3 短
    for _ in range(3):
        signal(DOT)

try:
    send_sos()

except KeyboardInterrupt:
    print("\n已停止 SOS")

finally:
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.output(BUZZER_PIN, GPIO.LOW)

    if buzzer is not None:
        buzzer.stop()
        buzzer = None
