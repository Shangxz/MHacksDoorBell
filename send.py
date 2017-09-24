import requests

url = "http://13.92.254.54:8080/api"

payload = "{\"url\":\"https://s3.amazonaws.com/mhacksxgmss/fedex.jpeg\"}"
headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "58ac7346-f1cd-3e29-869f-b6bb34eadc75"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
