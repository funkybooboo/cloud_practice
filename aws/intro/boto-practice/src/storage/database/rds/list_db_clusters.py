#!/usr/bin/env python3

import boto3
from mypy_boto3_rds.client import RDSClient

def list_db_clusters() -> None:
    client: RDSClient = boto3.client("rds")
    resp = client.describe_db_clusters()
    print("🗄️ RDS DB Clusters:")
    for c in resp["DBClusters"]:
        print(f" - {c['DBClusterIdentifier']} | Engine: {c['Engine']} | Status: {c['Status']}")

if __name__ == "__main__":
    list_db_clusters()
