import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    instance_id = event['detail']['instance-id']
    ec2.create_tags(
        Resources=[instance_id],
        Tags=[
            {'Key': 'Environment', 'Value': 'Production'},
            {'Key': 'Owner', 'Value': 'DevOpsTeam'}
        ]
    )
    return {'statusCode': 200, 'body': f'Tags added to {instance_id}'}
