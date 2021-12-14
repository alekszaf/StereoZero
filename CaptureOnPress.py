from gpiozero import Button
from picamera import PiCamera
from datetime import datetime
from signal import pause

button = Button(6)
camera = PiCamera()

def capture():
        tstamp = datetime.now()
        print(f'Capturing image @{datetime.now()}')
        camera.capture('/home/pi/Timelapse/left_%s.png' %tstamp)

camera.start_preview()
button.when_pressed = capture

pause()
    