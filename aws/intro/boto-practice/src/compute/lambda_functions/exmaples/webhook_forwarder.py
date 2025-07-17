import requests

def lambda_handler(event, context):
    target_url = 'https://thirdparty.api/endpoint'
    response = requests.post(target_url, json=event)
    return {'statusCode': 200, 'body': 'Forwarded'}
