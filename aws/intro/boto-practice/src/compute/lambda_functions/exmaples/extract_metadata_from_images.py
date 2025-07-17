import subprocess

def lambda_handler(event, context):
    image_path = "/tmp/image.jpg"
    with open(image_path, "wb") as f:
        f.write(event['image_bytes'])

    result = subprocess.run(['exiftool', image_path], capture_output=True, text=True)
    return {'statusCode': 200, 'body': result.stdout}
