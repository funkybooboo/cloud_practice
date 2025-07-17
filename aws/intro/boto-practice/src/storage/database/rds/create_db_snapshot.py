#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_rds.client import RDSClient

def create_db_snapshot(db_identifier: str, snapshot_id: str) -> None:
    client: RDSClient = boto3.client("rds")
    try:
        client.create_db_snapshot(DBSnapshotIdentifier=snapshot_id, DBInstanceIdentifier=db_identifier)
        print(f"✅ Creating snapshot '{snapshot_id}' for DB '{db_identifier}'")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: create_db_snapshot.py <db-identifier> <snapshot-id>")
        sys.exit(1)
    create_db_snapshot(sys.argv[1], sys.argv[2])
