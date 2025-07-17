import boto3
import datetime

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    volume_id = event['volume_id']
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S')
    snapshot = ec2.create_snapshot(
        VolumeId=volume_id,
        Description=f"Auto snapshot at {timestamp}"
    )
    return {'statusCode': 200, 'body': f'Snapshot created: {snapshot["SnapshotId"]}'}
