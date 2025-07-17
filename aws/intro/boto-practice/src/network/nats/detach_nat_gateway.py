#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client
from botocore.exceptions import ClientError


def detach_nat_gateway(nat_gateway_id: str) -> None:
    ec2: EC2Client = boto3.client("ec2")

    try:
        # Get NAT Gateway details to find the associated AllocationId
        nat_info = ec2.describe_nat_gateways(NatGatewayIds=[nat_gateway_id])
        gateway = nat_info["NatGateways"][0]
        allocation_id = gateway["NatGatewayAddresses"][0].get("AllocationId")

        # Delete the NAT Gateway
        print(f"🗑️ Deleting NAT Gateway: {nat_gateway_id}")
        ec2.delete_nat_gateway(NatGatewayId=nat_gateway_id)

        # Release the associated Elastic IP if it exists
        if allocation_id:
            print(f"🗑️ Releasing Elastic IP: {allocation_id}")
            ec2.release_address(AllocationId=allocation_id)

        print("✅ NAT Gateway detached and Elastic IP released.")

    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: detach_nat_gateway.py <nat-gateway-id>")
        sys.exit(1)

    detach_nat_gateway(sys.argv[1])
