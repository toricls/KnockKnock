import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

max = 10
i = 0
while i < max:
    GPIO.output(7, 1)
    time.sleep(1)
    GPIO.output(7, 0)
    time.sleep(1)
    i += 1

GPIO.cleanup()
