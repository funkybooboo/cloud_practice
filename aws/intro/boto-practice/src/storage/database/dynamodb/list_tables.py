#!/usr/bin/env python3

import boto3
from mypy_boto3_dynamodb.client import DynamoDBClient

def list_tables() -> None:
    client: DynamoDBClient = boto3.client("dynamodb")
    resp = client.list_tables()
    if not resp.get("TableNames"):
        print("⚠️ No DynamoDB tables found.")
    else:
        print("📋 DynamoDB Tables:")
        for name in resp["TableNames"]:
            print(f" - {name}")

if __name__ == "__main__":
    list_tables()
