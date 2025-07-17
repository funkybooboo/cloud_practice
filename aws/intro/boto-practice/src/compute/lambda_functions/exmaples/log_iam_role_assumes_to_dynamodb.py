import boto3
import time

ddb = boto3.resource('dynamodb').Table('IamAssumeLogs')

def lambda_handler(event, context):
    log = {
        'role': event['detail']['requestParameters']['roleArn'],
        'principal': event['detail']['userIdentity']['arn'],
        'timestamp': str(int(time.time()))
    }
    ddb.put_item(Item=log)
    return {'statusCode': 200, 'body': 'Log written'}
