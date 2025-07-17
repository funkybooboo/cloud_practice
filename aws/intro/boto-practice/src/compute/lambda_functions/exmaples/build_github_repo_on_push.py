import os
import subprocess

def lambda_handler(event, context):
    repo = event['repo']
    subprocess.run(['git', 'clone', repo, '/tmp/repo'])
    subprocess.run(['npm', 'install'], cwd='/tmp/repo')
    subprocess.run(['npm', 'run', 'build'], cwd='/tmp/repo')
    return {'statusCode': 200, 'body': 'Build completed'}
