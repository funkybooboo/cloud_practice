#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_rds.client import RDSClient

def create_db_cluster_instance(
    cluster_id: str,
    instance_id: str,
    instance_class: str
) -> None:
    client: RDSClient = boto3.client("rds")
    try:
        resp = client.create_db_instance(
            DBClusterIdentifier=cluster_id,
            DBInstanceIdentifier=instance_id,
            DBInstanceClass=instance_class,
            Engine="aurora"  # or "aurora-mysql" / "aurora-postgresql"
        )
        print(f"✅ Creating Cluster Instance: {resp['DBInstance']['DBInstanceIdentifier']}")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: create_db_cluster_instance.py <cluster-id> <instance-id> <instance-class>")
        sys.exit(1)
    create_db_cluster_instance(sys.argv[1], sys.argv[2], sys.argv[3])
