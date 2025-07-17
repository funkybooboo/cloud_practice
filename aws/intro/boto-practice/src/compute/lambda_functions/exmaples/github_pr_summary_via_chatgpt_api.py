import openai
import os
import requests

openai.api_key = os.environ['OPENAI_API_KEY']

def lambda_handler(event, context):
    diff = event['diff']
    summary = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Summarize this pull request diff:\n\n{diff}"}]
    )
    return {'statusCode': 200, 'body': summary.choices[0].message['content']}
