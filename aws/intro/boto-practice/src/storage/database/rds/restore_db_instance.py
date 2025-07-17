#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_rds.client import RDSClient

def restore_db_instance(new_identifier: str, snapshot_id: str) -> None:
    client: RDSClient = boto3.client("rds")
    try:
        client.restore_db_instance_from_db_snapshot(
            DBInstanceIdentifier=new_identifier,
            DBSnapshotIdentifier=snapshot_id,
            PubliclyAccessible=False
        )
        print(f"✅ Restoring DB from snapshot '{snapshot_id}' as '{new_identifier}'")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: restore_db_instance.py <new-identifier> <snapshot-id>")
        sys.exit(1)
    restore_db_instance(sys.argv[1], sys.argv[2])
