import boto3
import requests
import os

route53 = boto3.client('route53')
hosted_zone_id = os.environ['HOSTED_ZONE_ID']
record_name = os.environ['RECORD_NAME']

def lambda_handler(event, context):
    ip = requests.get("https://checkip.amazonaws.com/").text.strip()
    response = route53.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Changes': [{
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': record_name,
                    'Type': 'A',
                    'TTL': 300,
                    'ResourceRecords': [{'Value': ip}]
                }
            }]
        }
    )
    return {'statusCode': 200, 'body': f'Updated {record_name} to {ip}'}
