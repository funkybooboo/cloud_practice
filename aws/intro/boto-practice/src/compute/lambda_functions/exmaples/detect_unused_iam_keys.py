import boto3

sns = boto3.client('sns')

def lambda_handler(event, context):
    users = iam.list_users()['Users']
    inactive = []
    for user in users:
        keys = iam.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata']
        for key in keys:
            last_used = iam.get_access_key_last_used(AccessKeyId=key['AccessKeyId'])
            if 'LastUsedDate' not in last_used['AccessKeyLastUsed']:
                inactive.append(key)
    return {'statusCode': 200, 'body': inactive}
