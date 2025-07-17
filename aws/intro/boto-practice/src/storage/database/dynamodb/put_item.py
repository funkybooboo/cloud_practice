#!/usr/bin/env python3

import sys
import json
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.client import DynamoDBClient

def put_item(table_name: str, item_json: str) -> None:
    client: DynamoDBClient = boto3.client("dynamodb")
    item = json.loads(item_json)
    try:
        client.put_item(TableName=table_name, Item={k: {"S": str(v)} for k, v in item.items()})
        print(f"✅ Put item into {table_name}: {item}")
    except ClientError as e:
        print(f"❌ Error putting item: {e.response['Error']['Message']}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: put_item.py <table-name> '<json-item>'")
        sys.exit(1)
    put_item(sys.argv[1], sys.argv[2])
