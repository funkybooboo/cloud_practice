#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_rds.client import RDSClient

def stop_db_cluster(cluster_id: str, skip_final_snapshot: bool = True) -> None:
    """
    Stops an Aurora Serverless v1/v2 cluster.
    If skip_final_snapshot is False, you must specify --no-skip-final-snapshot.
    """
    client: RDSClient = boto3.client("rds")
    try:
        client.stop_db_cluster(
            DBClusterIdentifier=cluster_id,
            SkipFinalSnapshot=skip_final_snapshot
        )
        print(f"⏹️ Stopping Aurora cluster: {cluster_id}")
    except ClientError as e:
        print(f"❌ Error stopping cluster {cluster_id}: {e.response['Error']['Message']}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) not in (2,3):
        print("Usage: stop_db_cluster.py <cluster-id> [--no-skip-final-snapshot]")
        sys.exit(1)

    skip = True
    if len(sys.argv) == 3 and sys.argv[1] == "--no-skip-final-snapshot":
        # user passed flag first by mistake
        skip = False
        cluster = sys.argv[2]
    elif len(sys.argv) == 3 and sys.argv[2] == "--no-skip-final-snapshot":
        cluster = sys.argv[1]
        skip = False
    else:
        cluster = sys.argv[1]

    stop_db_cluster(cluster, skip)
