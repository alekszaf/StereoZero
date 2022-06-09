from gpiozero import Button
from picamera import PiCamera
from datetime import datetime
from signal import pause

button = Button(6)
camera = PiCamera()
camera.resolution = (720, 480)
camera.awb_mode = 'off'
camera.awb_gains = (1.0, 1.0)
camera.iso = 200
#camera.start_preview(fullscreen=False, window=(100,20,640,480))

frame = 1

while True:
    try:
        button.wait_for_press()
        camera.capture('/home/pi/Timelapse/frame%03d.png' % frame)
        frame += 1
    except KeyboardInterrupt:
        camera.stop_preview()
        break