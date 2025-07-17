import boto3

sns = boto3.client('sns')

def lambda_handler(event, context):
    topic_arn = event['topic_arn']
    message = event['message']
    sns.publish(TopicArn=topic_arn, Message=message)
    return {'statusCode': 200, 'body': 'Message published'}
