import base64
import json
import io
import time
import picamera
import cv2
import numpy
import requests

n=0
while n<10:
 stream = io.BytesIO()
 with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.capture(stream, format='jpeg')
 buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)
 image = cv2.imdecode(buff, 1)
 face_cascade = cv2.CascadeClassifier('/home/pi/Desktop/pilocal/faces.xml')
 gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
 faces = face_cascade.detectMultiScale(gray, 1.1, 5)
 print "Found "+str(len(faces))+" face(s)"
 for (x,y,w,h) in faces:
    cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
 cv2.imwrite('result'+str(n)+'.jpg',image)
 n=n+1
 stream.close()
cv2.destroyAllWindows()
