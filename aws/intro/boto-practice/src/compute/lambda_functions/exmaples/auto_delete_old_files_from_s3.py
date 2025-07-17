import boto3
from datetime import datetime, timezone, timedelta
import os

s3 = boto3.client('s3')
bucket = os.environ['BUCKET']
prefix = os.environ.get('PREFIX', '')
days_old = int(os.environ.get('DAYS_OLD', 30))

def lambda_handler(event, context):
    threshold = datetime.now(timezone.utc) - timedelta(days=days_old)
    deleted = []

    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    for obj in response.get('Contents', []):
        if obj['LastModified'] < threshold:
            s3.delete_object(Bucket=bucket, Key=obj['Key'])
            deleted.append(obj['Key'])

    return {
        'statusCode': 200,
        'body': f'Deleted {len(deleted)} objects: {deleted}'
    }
