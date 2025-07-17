#!/usr/bin/env python3

import boto3
from mypy_boto3_lambda.client import LambdaClient

def list_lambdas() -> None:
    client: LambdaClient = boto3.client("lambda")
    paginator = client.get_paginator("list_functions")
    print("🛠️ Lambda Functions:")
    for page in paginator.paginate():
        for fn in page["Functions"]:
            print(f" - {fn['FunctionName']} (Runtime: {fn['Runtime']}, ARN: {fn['FunctionArn']})")

if __name__ == "__main__":
    list_lambdas()
