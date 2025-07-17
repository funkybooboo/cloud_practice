#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_rds.client import RDSClient

def describe_db_cluster_endpoints(cluster_id: str) -> None:
    """
    Lists reader and writer endpoints for an Aurora cluster.
    """
    client: RDSClient = boto3.client("rds")
    resp = client.describe_db_clusters(DBClusterIdentifier=cluster_id)
    clusters = resp.get("DBClusters", [])
    if not clusters:
        print(f"⚠️ No cluster found with ID {cluster_id}")
        sys.exit(1)

    cluster = clusters[0]
    writer = cluster.get("Endpoint")
    reader = cluster.get("ReaderEndpoint")
    members = [m["DBInstanceIdentifier"] for m in cluster.get("DBClusterMembers", [])]
    print(f"🔗 Cluster '{cluster_id}' Endpoints:")
    print(f" - Writer endpoint: {writer}")
    print(f" - Reader endpoint: {reader or 'none'}")
    print(f" - Instances: {', '.join(members)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: describe_db_cluster_endpoints.py <cluster-id>")
        sys.exit(1)
    describe_db_cluster_endpoints(sys.argv[1])
