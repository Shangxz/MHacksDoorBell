# Python Dependencies
# ===================
import base64
import json

# 3rd Party Dependencies
# ======================
import requests

# Globals
# =======
url = 'https://xry68cyt39.execute-api.us-east-1.amazonaws.com/api/identify'

def uploadImage(fileName):

	with open(fileName, "rb") as f:
		e = base64.urlsafe_b64encode(f.read())
		headers = {'Content-type': 'application/json'}
		return requests.post(url, data=e, headers=headers).text

if __name__ == '__main__':
	print uploadImage('photoG.jpg')