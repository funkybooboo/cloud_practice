import boto3
import requests
from requests_aws4auth import AWS4Auth
import os

region = os.environ['AWS_REGION']
host = os.environ['OS_ENDPOINT']
index = os.environ['INDEX']
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

def lambda_handler(event, context):
    doc = event['document']
    response = requests.post(f"{host}/{index}/_doc/", auth=awsauth, json=doc)
    return {'statusCode': 200, 'body': response.json()}
