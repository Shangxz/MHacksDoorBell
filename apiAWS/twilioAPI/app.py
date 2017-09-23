from chalice import Chalice
from twilio.rest import Client

app = Chalice(app_name='twilioAPI')


@app.route('/')
def index():
    return {'hello': 'world'}

@app.lambda_function(name='twilio')
def twilio(event,context):
	try:
		name = " {} ".format(event['name'])
	except:
		name = " NONAME "

	account_sid = "AC860784c18e17afcac039126142104dae"
	# Your Auth Token from twilio.com/console
	auth_token  = "46fbd1cfaf1bae57c6fc2f0d7115f5b6"

	client = Client(account_sid, auth_token)

	message = client.messages.create(
	    to="+16266644912", 
	    from_="+13132511559",
	    body=name+"is at your door!")

	return {"message":message.sid}


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
