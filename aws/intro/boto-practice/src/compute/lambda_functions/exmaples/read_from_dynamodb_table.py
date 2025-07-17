import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MyTable')

def lambda_handler(event, context):
    key = {'id': event['id']}
    response = table.get_item(Key=key)
    return {'statusCode': 200, 'body': response.get('Item')}
