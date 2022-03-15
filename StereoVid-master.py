'''This is the main script for video recording'''

import RPi.GPIO as GPIO
from datetime import datetime
from picamera import PiCamera
from time import sleep

#Set button GPIO
button = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(button, GPIO.FALLING, bouncetime=300)

video_on = False

while True:
    if GPIO.event_detected(button):
        video_on = not video_on
        
    if video_on:
        
        #Initialize the camera with parameters of choice
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.awb_mode = 'off'
        camera.awb_gains = (1.1, 1.1)
        camera.iso = 200
        camera.shutter_speed = 10000
        camera.framerate = 20
        
        #Create the video file and start recording
        tstamp = datetime.now()
        camera.start_recording('/home/pi/Timelapse/video_%s.h264' %tstamp)
        print(f'Recording started @{datetime.now()}')
        
        #Record for a given period of time
        camera.wait_recording(20)
        print(f'Recording complete @{datetime.now()}')
        camera.stop_recording()
        
        #Shut down the camera
        camera.close()
        
        #Wait till the next capture
        sleep(600)