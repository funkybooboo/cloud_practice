#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client
from botocore.exceptions import ClientError


def create_subnet(vpc_id: str, cidr_block: str, az: str) -> None:
    ec2: EC2Client = boto3.client("ec2")
    try:
        response = ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock=cidr_block,
            AvailabilityZone=az,
            TagSpecifications=[{
                "ResourceType": "subnet",
                "Tags": [{"Key": "Name", "Value": "CustomSubnet"}]
            }]
        )
        subnet_id = response["Subnet"]["SubnetId"]
        print(f"✅ Created Subnet: {subnet_id} in AZ {az}")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: create_subnet.py <vpc-id> <cidr-block> <availability-zone>")
        sys.exit(1)

    create_subnet(sys.argv[1], sys.argv[2], sys.argv[3])
