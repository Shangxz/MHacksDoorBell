# Python Dependencies
# ===================
import base64
import json

# 3rd Party Dependencies
# ======================
import requests

# Globals
# =======
URL = 'https://xry68cyt39.execute-api.us-east-1.amazonaws.com/api/'

def uploadImage(fileName):

	url = URL + 'identify'

	with open(fileName, "rb") as f:
		e = base64.urlsafe_b64encode(f.read())
		headers = {'Content-type': 'application/json'}
		return requests.post(url, data=e, headers=headers).text

def trainModel(fileName,person):

	url = URL + 'trainPhotos'

	with open(fileName, "rb") as f:
		e = base64.urlsafe_b64encode(f.read())
		payload = {"name":person,"file":e}
		headers = {'Content-type': 'application/json'}
		return requests.post(url, data=json.dumps(payload), headers=headers).text


def shangAPI(fileName):
	url = 'http://13.92.254.54:8080/face'
	with open(fileName, "rb") as f:
		#e = str(int(f.read(), 8))
		e = base64.urlsafe_b64encode(f.read())
		#print e
		#payload = {"":""}
		headers = {'Content-type': 'application/json'}
		return requests.post(url, data=e, headers=headers).text




if __name__ == '__main__':
	print shangAPI('shang.jpg')
	#print uploadImage('photoG.jpg')
	#print trainModel('photoG.jpg','Griffin Miller')








