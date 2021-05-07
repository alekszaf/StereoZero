import RPi.GPIO as GPIO
from datetime import datetime
from picamera import PiCamera

#camera = PiCamera()

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

#GPIO.add_event_detect(20, GIO.RISING)

#i = 0

while True:
#    if GPIO.event_detected(20):
#         i += 1
#         tstamp = datetime.now()
#         print(f'Rising edge @{datetime.now()}')
#         camera.capture('/home/pi/Timelapse/testim%s.jpg' %tstamp)
#         if i == 10:
#             break
    if not GPIO.input(17):
        print('Port 17 is low')
         