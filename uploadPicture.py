# Python Dependencies
# ===================
import base64
import json
import time
import io
import picamera
import cv2
import numpy
import requests
import boto3


# 3rd Party Dependencies
# ======================

# Globals
# =======
url = 'https://xry68cyt39.execute-api.us-east-1.amazonaws.com/api/identify'
azureurl = "http://13.92.254.54:8080/api"
success = 0

def watch():
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.capture(stream, format='jpeg')
    buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)
    image = cv2.imdecode(buff, 1)
    face_cascade = cv2.CascadeClassifier('/home/pi/Desktop/pilocal/faces.xml')
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    print "watching..."
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
    cv2.imwrite('watch.jpg',image)
    if len(faces) == 1:
        print "hello!"
        return True
    else:
        return False
        
    stream.close()

def capture():
    attempts = 0
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
        if len(faces) == 1:
            req = uploadImage('result'+str(n)+'.jpg')
            if req:
                print "alerted user. going to sleep..."
                return True
            else:
                attempts+=1
            if attempts > 1:
                return False
            
        n=n+1
        stream.close()
    print "capture done"
    return True


def uploadImage(fileName):
    with open(fileName, "rb") as f:
        e = base64.urlsafe_b64encode(f.read())
        headers = {'Content-type': 'application/json'}
        x = requests.post(url, data=e, headers=headers).text
    uploadImageToS3(fileName)
    #print x
    return x

def uploadImageToS3(fileName):
    s3 = boto3.client('s3')
    print s3.upload_file(fileName, "mhacksxgmss", fileName)
    s3url = "https://s3.amazonaws.com/mhacksxgmss/"+fileName
    print s3url
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "58ac7346-f1cd-3e29-869f-b6bb34eadc75"
        }
    payload = json.dumps({"url":s3url})
    data = requests.request("POST", azureurl, data=payload, headers=headers).text
    
    dynamodb = boto3.resource("dynamodb")
    actionstable=dynamodb.Table("actions")
    actionstable.put_item(Item={"action":1,"description":data})
    
    return

if __name__ == '__main__':
    #print uploadImage('photoG.jpg')
    #capture()
    #uploadImageToS3("result0.jpg")
    while True:
        if watch():
            capture()
            time.sleep(10)
    