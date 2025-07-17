#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client
from botocore.exceptions import ClientError


def create_vpc(cidr_block: str) -> None:
    ec2: EC2Client = boto3.client("ec2")
    try:
        response = ec2.create_vpc(
            CidrBlock=cidr_block,
            TagSpecifications=[{
                "ResourceType": "vpc",
                "Tags": [{"Key": "Name", "Value": "CustomVPC"}]
            }]
        )
        vpc_id = response["Vpc"]["VpcId"]
        ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={"Value": True})
        ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={"Value": True})
        print(f"✅ Created VPC: {vpc_id} with CIDR block {cidr_block}")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: create_vpc.py <cidr-block>")
        sys.exit(1)

    create_vpc(sys.argv[1])
