import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    volumes = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
    deleted = []

    for vol in volumes['Volumes']:
        ec2.delete_volume(VolumeId=vol['VolumeId'])
        deleted.append(vol['VolumeId'])

    return {'statusCode': 200, 'body': f'Deleted volumes: {deleted}'}
