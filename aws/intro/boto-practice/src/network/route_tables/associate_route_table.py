#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client
from botocore.exceptions import ClientError


def associate_route_table(rt_id: str, subnet_id: str) -> None:
    ec2: EC2Client = boto3.client("ec2")
    try:
        ec2.associate_route_table(
            RouteTableId=rt_id,
            SubnetId=subnet_id
        )
        print(f"🔗 Associated Route Table {rt_id} with Subnet {subnet_id}")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: associate_route_table.py <route-table-id> <subnet-id>")
        sys.exit(1)

    associate_route_table(sys.argv[1], sys.argv[2])
