import boto3

lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    response = lambda_client.invoke(
        FunctionName='other-lambda-name',
        InvocationType='Event',
        Payload=b'{}'
    )
    return {'statusCode': 200, 'body': 'Triggered other lambda'}
