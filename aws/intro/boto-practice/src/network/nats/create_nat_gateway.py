#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client
from botocore.exceptions import ClientError


def create_nat_gateway(subnet_id: str, allocation_id: str) -> None:
    ec2: EC2Client = boto3.client("ec2")
    try:
        response = ec2.create_nat_gateway(
            SubnetId=subnet_id,
            AllocationId=allocation_id,
            TagSpecifications=[{
                "ResourceType": "natgateway",
                "Tags": [{"Key": "Name", "Value": "CustomNATGateway"}]
            }]
        )
        nat_id = response["NatGateway"]["NatGatewayId"]
        print(f"✅ Created NAT Gateway: {nat_id}")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: create_nat_gateway.py <subnet-id> <allocation-id>")
        sys.exit(1)

    create_nat_gateway(sys.argv[1], sys.argv[2])
