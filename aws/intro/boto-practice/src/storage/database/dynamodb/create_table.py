#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.client import DynamoDBClient

def create_table(
    table_name: str,
    read_capacity: int,
    write_capacity: int
) -> None:
    client: DynamoDBClient = boto3.client("dynamodb")
    try:
        resp = client.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": read_capacity, "WriteCapacityUnits": write_capacity}
        )
        print(f"✅ Creating table '{table_name}', status: {resp['TableDescription']['TableStatus']}")
    except ClientError as e:
        print(f"❌ Error creating table: {e.response['Error']['Message']}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: create_table.py <table-name> <read-capacity> <write-capacity>")
        sys.exit(1)
    create_table(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
