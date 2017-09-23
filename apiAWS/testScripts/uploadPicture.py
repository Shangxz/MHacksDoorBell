# Python Dependencies
# ===================
import base64
import json
import io
import picamera
import cv2
import numpy
# 3rd Party Dependencies
import requests

# Globals
# =======
url = 'https://xry68cyt39.execute-api.us-east-1.amazonaws.com/api/identify'
'''stream = io.BytesIO()
with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.capture(stream, format='jpeg')
buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)
image = cv2.imdecode(buff, 1)
face_cascade = cv2.CascadeClassifier('~/Desktop/haarcascade_frontalface_alt.xml')
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.1, 5)
print "Found "+str(len(faces))+" face(s)"
for (x,y,w,h) in faces:
    cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
cv2.imwrite('result.jpg',image)'''
def uploadImage(fileName):

	with open(fileName, "rb") as f:
		e = base64.urlsafe_b64encode(f.read())
		headers = {'Content-type': 'application/json'}
		return requests.post(url, data=e, headers=headers).text

if __name__ == '__main__':
	print uploadImage('batman1.jpg')