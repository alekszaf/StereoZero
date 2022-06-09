'''This is the main script for video recording

awb_gains modes
1.2, 1.3 - indoor daylight


'''

import RPi.GPIO as GPIO
from datetime import datetime
from picamera import PiCamera
from time import sleep
import argparse

# Set command line input for the video length
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--time", required = True, help = "Length of the video recording") 
args = vars(ap.parse_args())  # parse the arguments and store them in a dictionary

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
        camera.awb_gains = (1.3, 1.2)
        camera.iso = 100
        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = 'off'
        camera.framerate = 20
        
        #Create the video file and start recording
        tstamp = datetime.now()
        camera.start_recording('/home/pi/Timelapse/video_%s.h264' %tstamp)
        print(f'Recording started @{datetime.now()}')
        #camera.wait_recording(300)
        
        #Record for a given period of time
        camera.wait_recording(int(args["time"]))
        print(f'Recording complete @{datetime.now()}')
        camera.stop_recording()
        
        #Shut down the camera
        camera.close()
        
        #Wait till the next capture
        sleep(600)
        