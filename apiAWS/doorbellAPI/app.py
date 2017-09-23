# Python Dependencies
# ===================
import json
import uuid
import os
import base64

# 3rd Party Dependencies
# ======================
import requests

# AWS Dependencies
# ================
import boto3
from chalice import *

app = Chalice(app_name='doorbellAPI')
app.debug = True


s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')

rekognitionCollection = 'decibell'


@app.route('/')
def index():
    return {'hello': 'world'}



@app.route('/facebookUpload',methods=['POST'],content_types=['application/json'], cors=True)
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

		faceID = rekognition.index_faces(
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
				"PictureID": str(imageID),
				"rekognitionID": str(faceID)
				}
		)


	# delete files from temp
	for file in os.listdir('/tmp/'):
		os.remove('/tmp/'+file)

	return {"Success":True}


@app.route('/identify',methods=['POST'],content_types=['application/json'], cors=True)
def identify():
	event = json.loads(app.current_request.raw_body)

	bytearray=(base64.standard_b64decode(event["file"]))

	response = client.search_faces_by_image(
		CollectionId=rekognitionCollection,
		Image={
			'Bytes': buf
			},
		MaxFaces=1,
		FaceMatchThreshold=80
	)

	if len(response['FaceMatches']) == 0:
		return False
	else:
		res = response['FaceMatches'][0]['Face']['ExternalImageId']
		matchObj = re.match( r'(.*)_([0-9]+).jpg', res, re.M|re.I)
		if matchObj: return matchObj.group(1)
		else: return res






'''
@app.lambda_function(name='S3upload')
def s3upload(event,context):
	pass

'''








