#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_lambda.client import LambdaClient

def create_lambda(
    function_name: str,
    role_arn: str,
    handler: str,
    runtime: str,
    s3_bucket: str,
    s3_key: str
) -> None:
    client: LambdaClient = boto3.client("lambda")
    try:
        resp = client.create_function(
            FunctionName=function_name,
            Runtime=runtime,
            Role=role_arn,
            Handler=handler,
            Code={"S3Bucket": s3_bucket, "S3Key": s3_key},
            Publish=True
        )
        print(f"✅ Created Lambda: {resp['FunctionArn']}")
    except ClientError as e:
        print(f"❌ Error creating Lambda: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: create_lambda.py <function-name> <role-arn> <handler> <runtime> <s3-bucket> <s3-key>")
        sys.exit(1)
    create_lambda(*sys.argv[1:])
