import numpy as np
import cv2
import time
import base64
import requests
import io
import json

#import the cascade for face detection
face_cascade = cv2.CascadeClassifier('/Users/Sapto/Desktop/Mhacksdoorbell1/faces.xml')
URL = 'https://xry68cyt39.execute-api.us-east-1.amazonaws.com/api/'
def trainModel(fileName,person):

    url = URL + 'trainPhotos'

    with open(fileName, "rb") as f:
        e = base64.urlsafe_b64encode(f.read())
        payload = {"name":person,"file":e}
        headers = {'Content-type': 'application/json'}
        return requests.post(url, data=json.dumps(payload), headers=headers).text

def TakeSnapshotAndSave():
    name1=raw_input("Enter your name")
    # access the webcam (every webcam has a number, the default is 0)
    cap = cv2.VideoCapture(0)
    
    num = 0 
    while num<25:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # to detect faces in video
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

        x = 0
        y = 20
        text_color = (0,255,0)

        cv2.imwrite('opencv'+str(num)+'.jpg',frame)

        trainModel('opencv{}.jpg'.format(str(num)),name1)

        num = num+1

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    TakeSnapshotAndSave()
