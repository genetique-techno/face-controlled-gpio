from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import numpy
import cv2
import time
import math

# Do some stuff to set up the GPOI
print("---INITIALIZING GPIO")
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(40, GPIO.OUT, initial=GPIO.LOW)
power_state = False

# Set up the camera and get a reference to the camer
print("---INITIALIZING CAMERA")
camera = PiCamera()
camera.resolution = (1920, 1088)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(1920, 1088))

# let the camera warmup for
time.sleep(0.1)

# Load the face detection algorithm
print("---LOADING HAARCASCADE ALGORITHM")
face_cascade = cv2.CascadeClassifier("/home/pi/dev/cv-algs/haarcascade_frontalface_default.xml")


# cap = cv2.VideoCapture(0)
on_time = time.time()
initial_delay = on_time

print("---START CAPTURE LOOP")
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    delta = time.time() - on_time
    delay_time = time.time() - initial_delay
   
    if delta >= 1:

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        face = True if isinstance(faces, numpy.ndarray) else False

        if face:
            if power_state == False:
                print(time.time(), "POWERING ON")
            GPIO.output(40, GPIO.HIGH)
            power_state = True
            initial_delay = time.time()
        elif delay_time >= 10:
            if power_state == True:
                print(time.time(), "POWERING OFF")
                GPIO.output(40, GPIO.LOW)
                power_state = False
            initial_delay = time.time()

        on_time = time.time()
    
    # clear the stream for the next frame
    rawCapture.truncate(0)
    


