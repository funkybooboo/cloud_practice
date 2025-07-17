import boto3
cloudwatch = boto3.client('cloudwatch')
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    response = ec2.describe_instances()
    idle = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            id = instance['InstanceId']
            metrics = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': id}],
                StartTime=datetime.datetime.utcnow() - datetime.timedelta(days=7),
                EndTime=datetime.datetime.utcnow(),
                Period=3600 * 24,
                Statistics=['Average']
            )
            if metrics['Datapoints']:
                avg = sum(dp['Average'] for dp in metrics['Datapoints']) / len(metrics['Datapoints'])
                if avg < 5:
                    idle.append(id)

    return {'statusCode': 200, 'body': f'Idle Instances: {idle}'}
