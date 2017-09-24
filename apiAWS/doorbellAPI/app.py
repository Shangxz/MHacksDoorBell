# Python Dependencies
# ===================
import json
import uuid
import os
import base64
import time
import datetime as dt  

# 3rd Party Dependencies
# ======================
import requests

# AWS Dependencies
# ================
import boto3
from boto3.dynamodb.conditions import Key, Attr
from chalice import *

app = Chalice(app_name='doorbellAPI')
app.debug = True


s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
awsLambda = boto3.client('lambda')

rekognitionCollection = 'decibell'


@app.route('/trainPhotos',methods=['POST'],content_types=['application/json'], cors=True)
def trainPhotos():
	event = json.loads(app.current_request.raw_body)
	
	name = event["name"]

	file = bytearray(base64.urlsafe_b64decode(str(event["file"])))

	faceID = rekognition.index_faces(
		CollectionId=rekognitionCollection,
		Image={
			'Bytes': bytearray(file)
			},
	)["FaceRecords"][0]["Face"]["FaceId"]

	imageID = str(uuid.uuid4())

	table = dynamodb.Table('People')
	table.put_item(
		Item={
			"Name": str(name),
			"FaceID": str(faceID)
			}
	)

	return {"Success":True}



@app.route('/identify',methods=['POST'],content_types=['application/json'], cors=True)
def identify():

	buf=bytearray(base64.urlsafe_b64decode(app.current_request.raw_body))

	response = rekognition.search_faces_by_image(
		CollectionId=rekognitionCollection,
		Image={
			'Bytes': buf
			},
		MaxFaces=1,
		FaceMatchThreshold=50
	)

	if len(response['FaceMatches']) == 0:
		return False

	FaceID = response['FaceMatches'][0]['Face']['FaceId']

	table = dynamodb.Table('People')
	name = table.query(
		IndexName='FaceID-index',
		KeyConditionExpression=Key('FaceID').eq(FaceID)
	)["Items"][0]["Name"]

	table = dynamodb.Table('Here')
	table.put_item(
			Item={
				"date": str(dt.datetime.today().strftime("%m.%d.%Y")),
				"timestamp": str(int(time.time())),
				"name": str(name)
				}
		)

	awsLambda.invoke(
		FunctionName='twilioAPI-dev-twilio',
		InvocationType='Event',
		Payload=json.dumps({"name":str(name)})
	)

	return [response,int(time.time())]




'''
@app.route('/cdnUpload',methods=['POST'],content_types=['application/json'], cors=True)
def uploadToS3():
	event = json.loads(app.current_request.raw_body)['data']

	for pair in event:
		url = pair[0]
		name = pair[1]
		imageID = str(uuid.uuid4())
		imageIDfile = "{}.jpg".format(imageID)

		# download image to lambda files
		r = requests.get(url, allow_redirects=True)
		open('/tmp/'+imageIDfile, 'wb').write(r.content)

		# upload to s3
		with open('/tmp/'+imageIDfile, 'rb') as data:
			s3.upload_fileobj(data, 'mhacksdoorbell-trained', imageIDfile)

		FaceID = rekognition.index_faces(
			CollectionId=rekognitionCollection,
				Image={
					'S3Object': {
					'Bucket': 'mhacksdoorbell-trained',
					'Name': imageIDfile
					}
				},
			) ["FaceRecords"][0]["Face"]["FaceId"]

		# upload to dynamoDB
		table = dynamodb.Table('People')
		table.put_item(
			Item={
				"Name": str(name),
				"FaceID": str(FaceID),
				"rekognitionID": str(faceID)
				}
		)

	# delete files from temp
	for file in os.listdir('/tmp/'):
		os.remove('/tmp/'+file)

	return {"Success":True}
'''

