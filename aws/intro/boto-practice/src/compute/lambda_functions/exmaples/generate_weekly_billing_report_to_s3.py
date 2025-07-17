import boto3
import csv
import io
import datetime

ce = boto3.client('ce')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    start = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    end = datetime.datetime.utcnow().strftime('%Y-%m-%d')

    data = ce.get_cost_and_usage(
        TimePeriod={'Start': start, 'End': end},
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Service', 'Amount', 'Unit'])

    for group in data['ResultsByTime'][0]['Groups']:
        amount = group['Metrics']['UnblendedCost']['Amount']
        unit = group['Metrics']['UnblendedCost']['Unit']
        service = group['Keys'][0]
        writer.writerow([service, amount, unit])

    s3.put_object(Bucket='your-billing-bucket', Key='billing.csv', Body=output.getvalue())
    return {'statusCode': 200, 'body': 'Report uploaded to S3'}
