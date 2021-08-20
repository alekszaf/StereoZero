import RPi.GPIO as GPIO
import numpy as np
import cv2
from datetime import datetime
from picamera import PiCamera
from time import sleep

# Load parameters to recitfy images
cv_file = cv2.FileStorage()
cv_file.open('stereoMap.xml', cv2.FileStorage_READ)

stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()

# Initialize the camera
camera = PiCamera()
rawCapture = PiRGBArray(camera)

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Set GPIO to receive timer signal
channel = 4
GPIO.setup(channel, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(channel, GPIO.RISING)

i = 0
while True:
    if GPIO.event_detected(channel):

        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array

        # Rectify and undistort
        image = cv2.remap(image, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT)
        #image = cv2.remap(image, stereoMapR_x, stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT)
        
        tstamp = datetime.now()
        print(f'Rising edge detected @{datetime.now()}')
        camera.capture('/home/pi/Timelapse/green_calib%s.jpg' %tstamp)
        i += 1
        if i == 25:
            break


### Trigger with button

button = 17

KeepRunning = False

def buttonTrigger(button):
   GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
   GPIO.add_event_detect(button, GPIO.FALLING, bouncetime=300)
   if GPIO.event_detected(button):
       KeepRunning = True

def takeTimelapse(channel):
    while KeepRunning = True:
        if GPIO.event_detected(channel):
            tstamp = datetime.now()
            print(f'Rising edge detected @{datetime.now()}')
            camera.capture('/home/pi/Timelapse/green_calib%s.jpg' %tstamp)
