from datetime import datetime
from time import sleep
import tm1637

# BCM 編號：CLK = GPIO23（實體 Pin 16），DIO = GPIO24（實體 Pin 18）
display = tm1637.TM1637(clk=23, dio=24)
display.brightness = 4

show_colon = True

try:
    while True:
        now = datetime.now()
        digits = now.strftime("%H%M")

        segments = [tm1637.TM1637.encode_char(c) for c in digits]

        if show_colon:
            segments[1] |= 0x80

        display.write(segments)

        show_colon = not show_colon
        sleep(1)

except KeyboardInterrupt:
    display.write([0, 0, 0, 0])
    print("\n時鐘程式結束")
