import RPi.GPIO as GPIO
from datetime import datetime
from picamera import PiCamera
#from gpiozero import Button
from time import sleep

camera = PiCamera()

channel = 4

#button = Button(17)

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

#GPIO.add_event_detect(button, GPIO.RISING, bouncetime=300)
GPIO.add_event_detect(channel, GPIO.RISING)

#i = 0

while True:
    if GPIO.event_detected(channel):
        tstamp = datetime.now()
        #camera.capture('/home/pi/Timelapse/orange_test_%s.png' %tstamp)
        print(f'Rising edge @{datetime.now()}')
#        i += 1
#        if i == 10:
#            break