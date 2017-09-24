from __future__ import print_function

import json
def lambda_handler(event, context):
    pollyservice=boto3.client('polly')
    name = " {} ".format(event['name'])
    mytext='Welcome to our House'+name
    polly_response = polly_service.synthesize_speech(
    OutputFormat='mp3',
    Text=my_text,
    TextType='text',
    VoiceId='Emma' 
    )

    