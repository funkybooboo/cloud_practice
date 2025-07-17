import boto3

iam = boto3.client('iam')

def lambda_handler(event, context):
    username = event['username']
    keys = iam.list_access_keys(UserName=username)['AccessKeyMetadata']
    keys.sort(key=lambda x: x['CreateDate'])

    if len(keys) >= 2:
        iam.update_access_key(UserName=username,
                              AccessKeyId=keys[0]['AccessKeyId'],
                              Status='Inactive')
        iam.delete_access_key(UserName=username,
                              AccessKeyId=keys[0]['AccessKeyId'])

    new_key = iam.create_access_key(UserName=username)['AccessKey']
    return {
        'statusCode': 200,
        'body': {
            'AccessKeyId': new_key['AccessKeyId'],
            'SecretAccessKey': new_key['SecretAccessKey']
        }
    }
