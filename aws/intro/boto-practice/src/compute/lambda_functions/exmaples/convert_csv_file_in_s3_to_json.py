import boto3
import csv
import json
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['bucket']
    key = event['key']

    response = s3.get_object(Bucket=bucket, Key=key)
    lines = response['Body'].read().decode('utf-8').splitlines()
    reader = csv.DictReader(lines)
    data = list(reader)

    json_key = key.replace('.csv', '.json')
    s3.put_object(Bucket=bucket, Key=json_key, Body=json.dumps(data))

    return {'statusCode': 200, 'body': f'Converted to {json_key}'}
