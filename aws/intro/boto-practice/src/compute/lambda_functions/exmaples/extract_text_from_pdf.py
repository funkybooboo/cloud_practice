import boto3

textract = boto3.client('textract')

def lambda_handler(event, context):
    bucket = event['bucket']
    key = event['key']

    response = textract.detect_document_text(
        Document={'S3Object': {'Bucket': bucket, 'Name': key}}
    )

    text = '\n'.join([block['Text'] for block in response['Blocks'] if block['BlockType'] == 'LINE'])
    return {'statusCode': 200, 'body': text}
