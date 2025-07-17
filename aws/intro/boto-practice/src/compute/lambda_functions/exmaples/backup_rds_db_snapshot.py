import boto3
import datetime

rds = boto3.client('rds')

def lambda_handler(event, context):
    db_id = event['db_identifier']
    snapshot_id = f"{db_id}-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    rds.create_db_snapshot(DBSnapshotIdentifier=snapshot_id, DBInstanceIdentifier=db_id)
    return {'statusCode': 200, 'body': f'Snapshot {snapshot_id} created'}
