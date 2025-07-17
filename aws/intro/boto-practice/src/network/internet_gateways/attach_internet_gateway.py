#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client


def attach_igw(igw_id: str, vpc_id: str) -> None:
    ec2: EC2Client = boto3.client("ec2")
    ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
    print(f"🔗 Attached {igw_id} to VPC {vpc_id}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: attach_internet_gateway.py <igw-id> <vpc-id>")
        sys.exit(1)

    attach_igw(sys.argv[1], sys.argv[2])
