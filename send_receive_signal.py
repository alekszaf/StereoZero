import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(20, GPIO.IN)

while True:
    GPIO.output(26, 1)
    sleep(1)
    if GPIO.input(20):
        print('Port 20 is high')
    GPIO.output(26, 0)
    sleep(1)
    if not GPIO.input(20):
        print('Port 20 is low')