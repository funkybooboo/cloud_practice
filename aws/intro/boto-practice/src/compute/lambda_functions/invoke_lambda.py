#!/usr/bin/env python3

import sys
import json
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_lambda.client import LambdaClient

def invoke_lambda(function_name: str, payload: str) -> None:
    client: LambdaClient = boto3.client("lambda")
    try:
        resp = client.invoke(
            FunctionName=function_name,
            Payload=payload.encode("utf-8")
        )
        body = resp["Payload"].read().decode("utf-8")
        print(f"📨 Response payload:\n{json.dumps(json.loads(body), indent=2)}")
    except ClientError as e:
        print(f"❌ Error invoking Lambda: {e.response['Error']['Message']}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: invoke_lambda.py <function-name> <json-payload>")
        sys.exit(1)
    invoke_lambda(sys.argv[1], sys.argv[2])
