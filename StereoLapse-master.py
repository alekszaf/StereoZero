'''This is the main script used to take timelapse imagery'''

import RPi.GPIO as GPIO
from datetime import datetime
from picamera import PiCamera
from time import sleep

#Initialize the camera


#Set timer input GPIO
channel = 4

#Set button GPIO
button = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

GPIO.add_event_detect(channel, GPIO.RISING, bouncetime=100)
#GPIO.add_event_detect(button, GPIO.RISING, bouncetime=300)
GPIO.add_event_detect(button, GPIO.FALLING, bouncetime=300)

timelapse_on = False

while True:
    if GPIO.event_detected(button):
        timelapse_on = not timelapse_on
        
    if GPIO.event_detected(channel) and timelapse_on:
        camera = PiCamera()
        tstamp = datetime.now()
        print(f'Rising edge @{datetime.now()}')
        camera.capture('/home/pi/Timelapse/orange_10cm_%s.png' %tstamp)
        camera.close()

