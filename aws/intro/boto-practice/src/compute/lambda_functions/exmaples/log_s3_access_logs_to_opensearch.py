# triggered by S3 PUT of logs
def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    # Parse access log, transform into document, index in OpenSearch
    # You’d extract request info, IP, referrer, etc. and post to OpenSearch
