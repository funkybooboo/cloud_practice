import json
import boto3

sagemaker = boto3.client('sagemaker-runtime')

def lambda_handler(event, context):
    response = sagemaker.invoke_endpoint(
        EndpointName='your-endpoint',
        ContentType='application/json',
        Body=json.dumps(event['input'])
    )
    result = response['Body'].read().decode('utf-8')
    return {'statusCode': 200, 'body': result}
