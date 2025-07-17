#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_rds.client import RDSClient

def create_db_instance(
    db_identifier: str,
    db_instance_class: str,
    engine: str,
    master_username: str,
    master_password: str,
    allocated_storage: int,
    db_subnet_group: str,
    vpc_sg_ids: list[str]
) -> None:
    client: RDSClient = boto3.client("rds")
    try:
        resp = client.create_db_instance(
            DBInstanceIdentifier=db_identifier,
            DBInstanceClass=db_instance_class,
            Engine=engine,
            MasterUsername=master_username,
            MasterUserPassword=master_password,
            AllocatedStorage=allocated_storage,
            DBSubnetGroupName=db_subnet_group,
            VpcSecurityGroupIds=vpc_sg_ids,
            PubliclyAccessible=False
        )
        print(f"✅ Creating DB instance: {resp['DBInstance']['DBInstanceIdentifier']}")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 9:
        print(
            "Usage: create_db_instance.py "
            "<db-identifier> <db-class> <engine> <master-user> "
            "<master-pass> <storage-gb> <db-subnet-group> <sg1,sg2,...>"
        )
        sys.exit(1)

    subnet = sys.argv[7]
    sg_ids = sys.argv[8].split(",")
    create_db_instance(
        db_identifier=sys.argv[1],
        db_instance_class=sys.argv[2],
        engine=sys.argv[3],
        master_username=sys.argv[4],
        master_password=sys.argv[5],
        allocated_storage=int(sys.argv[6]),
        db_subnet_group=subnet,
        vpc_sg_ids=sg_ids
    )
