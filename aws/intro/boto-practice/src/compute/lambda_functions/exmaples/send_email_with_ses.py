import boto3
import os

ses = boto3.client('ses')
SENDER = os.environ['SENDER_EMAIL']
REGION = os.environ.get('AWS_REGION', 'us-east-1')

def lambda_handler(event, context):
    to_email = event['to']
    subject = event['subject']
    body = event['body']

    ses.send_email(
        Source=SENDER,
        Destination={'ToAddresses': [to_email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}}
        }
    )
    return {
        'statusCode': 200,
        'body': f'Email sent to {to_email}'
    }
