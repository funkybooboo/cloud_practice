import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MyTable')

def lambda_handler(event, context):
    item = event['item']  # should be a dict with valid keys
    table.put_item(Item=item)
    return {'statusCode': 200, 'body': 'Item inserted'}
