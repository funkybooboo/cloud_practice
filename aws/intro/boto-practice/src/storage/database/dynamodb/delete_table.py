#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.client import DynamoDBClient

def delete_table(table_name: str) -> None:
    client: DynamoDBClient = boto3.client("dynamodb")
    try:
        client.delete_table(TableName=table_name)
        print(f"🗑️ Deleted table: {table_name}")
    except ClientError as e:
        print(f"❌ Error deleting table: {e.response['Error']['Message']}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: delete_table.py <table-name>")
        sys.exit(1)
    delete_table(sys.argv[1])
