#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_rds.client import RDSClient

def delete_db_instance(db_identifier: str, skip_final_snapshot: bool = True) -> None:
    client: RDSClient = boto3.client("rds")
    try:
        client.delete_db_instance(
            DBInstanceIdentifier=db_identifier,
            SkipFinalSnapshot=skip_final_snapshot
        )
        print(f"🗑️ Deleting DB instance: {db_identifier}")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Usage: delete_db_instance.py <db-identifier> [--no-skip-final-snapshot]")
        sys.exit(1)

    skip = True
    if len(sys.argv) == 3 and sys.argv[2] == "--no-skip-final-snapshot":
        skip = False

    delete_db_instance(sys.argv[1], skip)
