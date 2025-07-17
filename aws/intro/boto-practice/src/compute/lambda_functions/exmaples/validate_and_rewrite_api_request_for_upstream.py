def lambda_handler(event, context):
    request = event['body']
    if 'email' not in request or not request['email'].endswith('@example.com'):
        return {'statusCode': 400, 'body': 'Unauthorized domain'}

    request['email'] = request['email'].lower()
    # forward to backend or enqueue
    return {'statusCode': 200, 'body': request}
