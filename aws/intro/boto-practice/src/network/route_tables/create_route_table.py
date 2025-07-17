#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client
from botocore.exceptions import ClientError


def create_route_table(vpc_id: str) -> None:
    ec2: EC2Client = boto3.client("ec2")
    try:
        response = ec2.create_route_table(
            VpcId=vpc_id,
            TagSpecifications=[{
                "ResourceType": "route-table",
                "Tags": [{"Key": "Name", "Value": "CustomRouteTable"}]
            }]
        )
        rt_id = response["RouteTable"]["RouteTableId"]
        print(f"✅ Created Route Table: {rt_id}")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: create_route_table.py <vpc-id>")
        sys.exit(1)

    create_route_table(sys.argv[1])
