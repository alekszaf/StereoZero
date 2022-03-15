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
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.awb_mode = 'off'
        camera.awb_gains = (1.1, 1.1)
        camera.iso = 200
        tstamp = datetime.now()
        camera.shutter_speed = 10000
        camera.framerate = 20
        camera.start_recording('/home/pi/Timelapse/video_%s' %tstamp, format='h264')
        print(f'Recording started @{datetime.now()}')
        camera.wait_recording(20)
        print(f'Recording complete @{datetime.now()}')
        camera.stop_recording()
        camera.close()
        sleep(60)