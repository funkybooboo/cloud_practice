import boto3
import time

cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
    metric_name = event['metric_name']
    value = event['value']
    namespace = event.get('namespace', 'Custom/Lambda')

    cloudwatch.put_metric_data(
        Namespace=namespace,
        MetricData=[
            {
                'MetricName': metric_name,
                'Timestamp': time.time(),
                'Value': value,
                'Unit': 'Count'
            },
        ]
    )

    return {'statusCode': 200, 'body': f'Metric {metric_name} pushed with value {value}'}
