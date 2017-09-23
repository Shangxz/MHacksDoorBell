from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "AC860784c18e17afcac039126142104dae"
# Your Auth Token from twilio.com/console
auth_token  = "46fbd1cfaf1bae57c6fc2f0d7115f5b6"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+13135306749", 
    from_="+13132511559",
    body="Hello from Python!")

print(message.sid)