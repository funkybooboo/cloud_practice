import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        s3.copy_object(
            Bucket=bucket,
            Key=key,
            CopySource={'Bucket': bucket, 'Key': key},
            StorageClass='GLACIER',
            MetadataDirective='COPY'
        )
    return {'statusCode': 200, 'body': 'Moved to Glacier'}
