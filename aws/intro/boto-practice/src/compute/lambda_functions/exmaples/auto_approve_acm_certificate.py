import boto3
import time

acm = boto3.client('acm')
route53 = boto3.client('route53')

def lambda_handler(event, context):
    cert_arn = event['CertificateArn']
    cert_details = acm.describe_certificate(CertificateArn=cert_arn)['Certificate']

    for option in cert_details['DomainValidationOptions']:
        record = option['ResourceRecord']
        hosted_zone = route53.list_hosted_zones_by_name(DNSName=record['Name'].rstrip('.'))['HostedZones'][0]
        route53.change_resource_record_sets(
            HostedZoneId=hosted_zone['Id'],
            ChangeBatch={
                'Changes': [{
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': record['Name'],
                        'Type': record['Type'],
                        'TTL': 300,
                        'ResourceRecords': [{'Value': record['Value']}]
                    }
                }]
            }
        )

    return {'statusCode': 200, 'body': f'DNS record created for validation'}
