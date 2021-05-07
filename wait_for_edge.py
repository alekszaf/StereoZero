'''This code works for detecting rising edge
    of the signal transmitted by the timer.
    
    BUGS:
        - two outputs within one second'''

import RPi.GPIO as GPIO
from datetime import datetime
from picamera import PiCamera
from time import sleep

channel = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

GPIO.add_event_detect(channel, GPIO.RISING)

while True:
    if GPIO.event_detected(channel):
        print(f'Rising edge @{datetime.now()}')