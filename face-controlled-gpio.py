import RPi.GPIO as GPIO
import numpy
import cv2
import time
import math

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(40, GPIO.OUT, initial=GPIO.LOW)
power_state = False

face_cascade = cv2.CascadeClassifier("/home/pi/dev/cv-algs/haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)
on_time = time.time()
initial_delay = on_time

while(True):
    delta = time.time() - on_time
    delay_time = time.time() - initial_delay
    ret, frame = cap.read()
    if delta >= 1:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
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


cap.release()
