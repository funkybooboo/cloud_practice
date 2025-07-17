import boto3

sns = boto3.client('sns')

def lambda_handler(event, context):
    phone = event['phone']
    message = event['message']
    sns.publish(PhoneNumber=phone, Message=message)
    return {'statusCode': 200, 'body': 'SMS sent'}
