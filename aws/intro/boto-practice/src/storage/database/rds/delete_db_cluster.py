#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_rds.client import RDSClient

def delete_db_cluster(cluster_id: str, skip_final_snapshot: bool = True) -> None:
    client: RDSClient = boto3.client("rds")
    try:
        client.delete_db_cluster(
            DBClusterIdentifier=cluster_id,
            SkipFinalSnapshot=skip_final_snapshot
        )
        print(f"🗑️ Deleting DB Cluster: {cluster_id}")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Usage: delete_db_cluster.py <cluster-id> [--no-skip-final-snapshot]")
        sys.exit(1)

    skip = True
    if len(sys.argv) == 3 and sys.argv[2] == "--no-skip-final-snapshot":
        skip = False

    delete_db_cluster(sys.argv[1], skip)
