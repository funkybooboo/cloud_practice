import boto3

logs = boto3.client('logs')

def lambda_handler(event, context):
    prefix = event.get('prefix', '')
    days = int(event.get('days', 30))
    log_groups = logs.describe_log_groups(logGroupNamePrefix=prefix)['logGroups']
    for group in log_groups:
        logs.put_retention_policy(logGroupName=group['logGroupName'], retentionInDays=days)
    return {'statusCode': 200, 'body': 'Retention policy updated'}
