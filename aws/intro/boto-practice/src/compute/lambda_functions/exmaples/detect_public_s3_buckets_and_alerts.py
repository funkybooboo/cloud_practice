import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    public_buckets = []
    for bucket in s3.list_buckets()['Buckets']:
        acl = s3.get_bucket_acl(Bucket=bucket['Name'])
        for grant in acl['Grants']:
            if grant['Grantee'].get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers':
                public_buckets.append(bucket['Name'])

    return {'statusCode': 200, 'body': f'Public buckets: {public_buckets}'}
