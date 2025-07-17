import boto3
import base64
import os

s3 = boto3.client('s3')
BUCKET = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    file_name = event['file_name']
    file_data = base64.b64decode(event['file_data'])  # Expect base64 input

    s3.put_object(Bucket=BUCKET, Key=file_name, Body=file_data)

    return {
        'statusCode': 200,
        'body': f'File {file_name} uploaded successfully to {BUCKET}'
    }
