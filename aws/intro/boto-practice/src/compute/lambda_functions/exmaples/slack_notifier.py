import requests
import os

SLACK_URL = os.environ['SLACK_WEBHOOK_URL']

def lambda_handler(event, context):
    message = event.get('message', 'No message provided')
    payload = {'text': message}
    requests.post(SLACK_URL, json=payload)
    return {'statusCode': 200, 'body': 'Message sent to Slack'}
