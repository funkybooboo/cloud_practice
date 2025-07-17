#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_lambda.client import LambdaClient

def delete_lambda(function_name: str) -> None:
    client: LambdaClient = boto3.client("lambda")
    try:
        client.delete_function(FunctionName=function_name)
        print(f"🗑️ Deleted Lambda: {function_name}")
    except ClientError as e:
        print(f"❌ Error deleting Lambda: {e.response['Error']['Message']}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: delete_lambda.py <function-name>")
        sys.exit(1)
    delete_lambda(sys.argv[1])
