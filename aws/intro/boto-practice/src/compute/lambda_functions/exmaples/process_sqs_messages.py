import boto3

sns = boto3.client('sns')

def lambda_handler(event, context):
    for record in event['Records']:
        print(f"Message received: {record['body']}")
    return {'statusCode': 200, 'body': f"Processed {len(event['Records'])} messages"}
