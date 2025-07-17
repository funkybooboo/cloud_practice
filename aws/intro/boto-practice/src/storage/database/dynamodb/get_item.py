#!/usr/bin/env python3

import sys
import boto3
import json
from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.client import DynamoDBClient

def get_item(table_name: str, key_value: str) -> None:
    client: DynamoDBClient = boto3.client("dynamodb")
    try:
        resp = client.get_item(TableName=table_name, Key={"id": {"S": key_value}})
        item = resp.get("Item")
        if not item:
            print(f"⚠️ No item found with id={key_value}")
        else:
            print("📦 Retrieved item:")
            print(json.dumps({k: list(v.values())[0] for k, v in item.items()}, indent=2))
    except ClientError as e:
        print(f"❌ Error getting item: {e.response['Error']['Message']}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: get_item.py <table-name> <id>")
        sys.exit(1)
    get_item(sys.argv[1], sys.argv[2])
