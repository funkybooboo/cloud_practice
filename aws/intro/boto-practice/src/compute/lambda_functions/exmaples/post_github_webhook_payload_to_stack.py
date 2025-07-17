import requests
import json
import os

SLACK_URL = os.environ['SLACK_WEBHOOK_URL']

def lambda_handler(event, context):
    payload = json.loads(event['body'])
    repo = payload['repository']['full_name']
    pusher = payload['pusher']['name']
    commit_msg = payload['head_commit']['message']

    msg = f"*Push to {repo}* by `{pusher}`\n> {commit_msg}"
    requests.post(SLACK_URL, json={'text': msg})
    return {'statusCode': 200, 'body': 'Posted to Slack'}
