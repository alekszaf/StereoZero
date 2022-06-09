from datetime import datetime
from picamera import PiCamera
from time import sleep
import numpy as np

camera = PiCamera()
frame=1

list = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5]

i = 0.1

while i < 1.9:
    camera.resolution = (640, 480)
    camera.awb_mode = 'off'
    camera.awb_gains = (1.3, i)
    camera.iso = 100
    camera.capture('/home/pi/Timelapse/awb_blue%s.png' %frame)
    print(str(frame) +" = " + str(i))
    frame += 1
    i += 0.1
    