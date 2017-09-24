import requests

url = 'https://scontent-ort2-2.xx.fbcdn.net/v/t1.0-1/p200x200/17200886_10211176263510073_4752187032452304708_n.jpg?oh=6dafe9e22f9d28ea96f9ad7f5ea4a290&oe=5A436CB8'
r = requests.get(url, allow_redirects=True)
open('test.jpg', 'wb').write(r.content)