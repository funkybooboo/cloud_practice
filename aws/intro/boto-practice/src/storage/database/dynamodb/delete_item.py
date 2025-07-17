#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.client import DynamoDBClient

def delete_item(table_name: str, key_value: str) -> None:
    client: DynamoDBClient = boto3.client("dynamodb")
    try:
        client.delete_item(TableName=table_name, Key={"id": {"S": key_value}})
        print(f"🗑️ Deleted item with id={key_value} from {table_name}")
    except ClientError as e:
        print(f"❌ Error deleting item: {e.response['Error']['Message']}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: delete_item.py <table-name> <id>")
        sys.exit(1)
    delete_item(sys.argv[1], sys.argv[2])
