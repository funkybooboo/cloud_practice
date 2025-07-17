def lambda_handler(event, context):
    token = event['authorizationToken']
    method_arn = event['methodArn']
    if token == "allow-this-token":
        effect = "Allow"
    else:
        effect = "Deny"

    return {
        "principalId": "user",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [{
                "Action": "execute-api:Invoke",
                "Effect": effect,
                "Resource": method_arn
            }]
        }
    }
