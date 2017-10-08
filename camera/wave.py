import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(26, GPIO.OUT)
p = GPIO.PWM(26, 0.5)
pwm = GPIO.PWM(26, 50)

pwm.start(5)

max = 10
i = 0
while i < max:
	pwm.ChangeDutyCycle(2)
	time.sleep(0.5)
	pwm.ChangeDutyCycle(6)
	time.sleep(0.5)
	i += 1

GPIO.cleanup()
