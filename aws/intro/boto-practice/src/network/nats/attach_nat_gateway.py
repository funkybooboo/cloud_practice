#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client
from botocore.exceptions import ClientError


def attach_nat_gateway(subnet_id: str) -> None:
    ec2: EC2Client = boto3.client("ec2")

    try:
        # Step 1: Allocate an Elastic IP
        eip_response = ec2.allocate_address(Domain="vpc")
        allocation_id = eip_response["AllocationId"]
        public_ip = eip_response["PublicIp"]
        print(f"📡 Allocated Elastic IP: {public_ip} ({allocation_id})")

        # Step 2: Create NAT Gateway in the public subnet
        nat_response = ec2.create_nat_gateway(
            SubnetId=subnet_id,
            AllocationId=allocation_id,
            TagSpecifications=[
                {
                    "ResourceType": "natgateway",
                    "Tags": [{"Key": "Name", "Value": "AttachedNATGateway"}]
                }
            ]
        )
        nat_gateway_id = nat_response["NatGateway"]["NatGatewayId"]
        print(f"✅ NAT Gateway created: {nat_gateway_id}")

    except ClientError as e:
        print(f"❌ AWS Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: attach_nat_gateway.py <subnet-id>")
        sys.exit(1)

    attach_nat_gateway(sys.argv[1])
