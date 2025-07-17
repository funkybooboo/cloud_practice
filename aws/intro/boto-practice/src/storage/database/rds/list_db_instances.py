#!/usr/bin/env python3

import boto3
from mypy_boto3_rds.client import RDSClient

def list_db_instances() -> None:
    client: RDSClient = boto3.client("rds")
    resp = client.describe_db_instances()
    print("🗄️ RDS Instances:")
    for inst in resp["DBInstances"]:
        print(f" - {inst['DBInstanceIdentifier']} | Engine: {inst['Engine']} | Status: {inst['DBInstanceStatus']}")

if __name__ == "__main__":
    list_db_instances()
