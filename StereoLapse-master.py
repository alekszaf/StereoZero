'''This is the main script used to take timelapse imagery'''

import RPi.GPIO as GPIO
from datetime import datetime
from picamera import PiCamera
from time import sleep

#Initialize the camera
#camera = PiCamera()

#Set timer input GPIO
channel = 5

#Set button GPIO
button = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

GPIO.add_event_detect(channel, GPIO.RISING, bouncetime=100)
GPIO.add_event_detect(button, GPIO.FALLING, bouncetime=300)

timelapse_on = False

while True:
    if GPIO.event_detected(button):
        timelapse_on = not timelapse_on
        
    if GPIO.event_detected(channel) and timelapse_on:
        camera = PiCamera()
        #camera.resolution = (2592, 1944)
        camera.resolution = (720, 480)
        camera.awb_mode = 'off'
        camera.awb_gains = (1.1, 1.1)
        camera.iso = 200
        tstamp = datetime.now()
        print(f'Rising edge @{datetime.now()}')
        camera.capture('/home/pi/Timelapse/left_%s.png' %tstamp)
        camera.close()

