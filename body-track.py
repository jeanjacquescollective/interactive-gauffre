#!/usr/bin/python3

import cv2
import os  
import time
from picamera2 import Picamera2
import time
import RPi.GPIO as GPIO



# download the cascade file from the link below
# https://github.com/opencv/opencv/blob/4.x/data/haarcascades/haarcascade_frontalface_default.xml

haar_upper_body_cascade = cv2.CascadeClassifier("./haarcascade_eye.xml")
cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

# Create a directory to store detected faces
output_directory = "detected_faces"
os.makedirs(output_directory, exist_ok=True)

width = 640
height = 480
currentactivePin = -1
outputPins = [2,2,2,2,3,3,3,3,3,3]
framesWithoutDetection = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

while True:
    frame = picam2.capture_array()
    img = cv2.resize(frame, (width, height))
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    upper_body = haar_upper_body_cascade.detectMultiScale(
        grey,
        scaleFactor = 1.05,
        minNeighbors = 6,
        minSize = (30, 30), # Min size for valid detection, changes according to video size or body size in the video.
        maxSize= (100,100),
        flags = cv2.CASCADE_SCALE_IMAGE
    )
    if len(upper_body) > 0:
    # for (x, y, w, h) in upper_body:
        framesWithoutDetection = 0
        (x, y, w, h) = upper_body[0]
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1) # creates green color rectangle with a thickness size of 1
        cv2.putText(img, "Upper Body Detected", (x + 5, y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2) # creates green color text with text size of 0.5 & thickness size of 2
        percentage_x = (x+w/2)/width
        pinCalculation = round(percentage_x * 10)
        if pinCalculation != currentactivePin:
            print("change")
            try:
                GPIO.output(outputPins[currentactivePin], False) 
            except:
                print("An exception occurred")
            currentactivePin = pinCalculation
            GPIO.output(outputPins[currentactivePin], True)
            print(outputPins[currentactivePin])
    else:
        framesWithoutDetection += 1
        if framesWithoutDetection >= 10:
            try:
                GPIO.output(outputPins[currentactivePin], False) 
            except:
                print("An exception occurred")
            currentactivePin = -1
    cv2.imshow('Video', img) # Display video
        # Generate a unique filename using timestamp for every saved image
        # timestamp = int(time.time())
        #    filename = os.path.join(output_directory, f"face_{timestamp}.jpg")
        # cv2.imwrite(filename, im[y:y+h, x:x+w])  # Save only the detected face portion
        

        # stop script when "q" key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        

# Release capture
video_capture.release()
cv2.destroyAllWindows()

