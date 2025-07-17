import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    action = event.get('action')  # 'start' or 'stop'
    filters = [{'Name': 'tag:AutoStartStop', 'Values': ['True']}]

    instances = ec2.describe_instances(Filters=filters)
    ids = [i['InstanceId']
           for r in instances['Reservations']
           for i in r['Instances']]

    if action == 'start':
        ec2.start_instances(InstanceIds=ids)
    elif action == 'stop':
        ec2.stop_instances(InstanceIds=ids)
    else:
        return {'statusCode': 400, 'body': 'Invalid action'}

    return {'statusCode': 200, 'body': f'{action.title()}ed instances: {ids}'}
