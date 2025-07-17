def lambda_handler(event, context):
    alarm_name = event['detail']['alarmName']
    new_state = event['detail']['state']['value']

    if new_state == 'ALARM':
        print(f"Alarm triggered: {alarm_name}")
        # (Optionally: send to Slack, SNS, email, etc.)

    return {'statusCode': 200, 'body': f'Handled alarm {alarm_name} in state {new_state}'}
