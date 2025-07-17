import jwt
import requests

def lambda_handler(event, context):
    token = event['token']
    keys_url = "https://cognito-idp.<region>.amazonaws.com/<userpool-id>/.well-known/jwks.json"
    jwks = requests.get(keys_url).json()

    header = jwt.get_unverified_header(token)
    key = next(k for k in jwks['keys'] if k['kid'] == header['kid'])
    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))

    payload = jwt.decode(token, public_key, algorithms=['RS256'], audience='<your-client-id>')
    return {'statusCode': 200, 'body': payload}
