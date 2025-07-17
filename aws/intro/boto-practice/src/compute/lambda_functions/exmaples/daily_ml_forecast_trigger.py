import boto3

sagemaker = boto3.client('sagemaker-runtime')

def lambda_handler(event, context):
    payload = {"input": "latest stats"}
    response = sagemaker.invoke_endpoint(
        EndpointName='forecast-endpoint',
        ContentType='application/json',
        Body=json.dumps(payload)
    )
    return {'statusCode': 200, 'body': response['Body'].read().decode()}
