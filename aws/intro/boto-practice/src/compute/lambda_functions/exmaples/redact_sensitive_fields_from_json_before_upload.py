import json
import boto3

s3 = boto3.client('s3')
REDACT_FIELDS = ['ssn', 'creditCardNumber', 'password']

def lambda_handler(event, context):
    data = event['record']
    redacted = {k: ('REDACTED' if k in REDACT_FIELDS else v) for k, v in data.items()}
    s3.put_object(Bucket='your-secure-bucket', Key='redacted.json', Body=json.dumps(redacted))
    return {'statusCode': 200, 'body': 'Redacted and saved'}
