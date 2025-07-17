import boto3
import os
import datetime

cloudfront = boto3.client('cloudfront')
DISTRIBUTION_ID = os.environ['CF_DISTRIBUTION_ID']

def lambda_handler(event, context):
    paths = event.get('paths', ['/*'])

    cloudfront.create_invalidation(
        DistributionId=DISTRIBUTION_ID,
        InvalidationBatch={
            'Paths': {
                'Quantity': len(paths),
                'Items': paths
            },
            'CallerReference': str(datetime.datetime.utcnow().timestamp())
        }
    )
    return {'statusCode': 200, 'body': f'Invalidation submitted for {paths}'}
