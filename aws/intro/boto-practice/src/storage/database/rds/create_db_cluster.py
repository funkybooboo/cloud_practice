#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_rds.client import RDSClient

def create_db_cluster(
    cluster_id: str,
    engine: str,
    master_username: str,
    master_password: str,
    db_subnet_group: str,
    vpc_sg_ids: list[str]
) -> None:
    client: RDSClient = boto3.client("rds")
    try:
        resp = client.create_db_cluster(
            DBClusterIdentifier=cluster_id,
            Engine=engine,
            MasterUsername=master_username,
            MasterUserPassword=master_password,
            DBSubnetGroupName=db_subnet_group,
            VpcSecurityGroupIds=vpc_sg_ids
        )
        print(f"✅ Creating DB Cluster: {resp['DBCluster']['DBClusterIdentifier']}")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            "Usage: create_db_cluster.py "
            "<cluster-id> <engine> <master-user> <master-pass> "
            "<db-subnet-group> <sg1,sg2,...>"
        )
        sys.exit(1)

    sg_list = sys.argv[5].split(",")
    create_db_cluster(
        cluster_id=sys.argv[1],
        engine=sys.argv[2],
        master_username=sys.argv[3],
        master_password=sys.argv[4],
        db_subnet_group=sys.argv[5],
        vpc_sg_ids=sg_list
    )
