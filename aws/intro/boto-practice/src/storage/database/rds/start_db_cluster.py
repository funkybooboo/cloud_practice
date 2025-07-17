#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_rds.client import RDSClient

def start_db_cluster(cluster_id: str) -> None:
    """
    Starts an Aurora Serverless v1/v2 cluster that was previously stopped.
    """
    client: RDSClient = boto3.client("rds")
    try:
        client.start_db_cluster(DBClusterIdentifier=cluster_id)
        print(f"▶️ Starting Aurora cluster: {cluster_id}")
    except ClientError as e:
        print(f"❌ Error starting cluster {cluster_id}: {e.response['Error']['Message']}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: start_db_cluster.py <cluster-id>")
        sys.exit(1)
    start_db_cluster(sys.argv[1])
