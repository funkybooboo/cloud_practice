from PIL import Image
import boto3
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key    = event['Records'][0]['s3']['object']['key']

    original = s3.get_object(Bucket=bucket, Key=key)['Body'].read()
    image = Image.open(io.BytesIO(original))
    image = image.resize((512, 512))

    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    buffer.seek(0)

    s3.put_object(Bucket=bucket, Key=f'resized/{key}', Body=buffer)
    return {'statusCode': 200, 'body': f'Image resized and saved to resized/{key}'}
