import time
import RPi.GPIO as GPIO

sleepytime = 1
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
while True:
    print('on')
    GPIO.output(2, True)
    time.sleep(sleepytime)
    print('off')
    GPIO.output(2, False)
    time.sleep(sleepytime)
