#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client


def detach_igw(igw_id: str, vpc_id: str) -> None:
    ec2: EC2Client = boto3.client("ec2")
    ec2.detach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
    print(f"🔌 Detached {igw_id} from VPC {vpc_id}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: detach_internet_gateway.py <igw-id> <vpc-id>")
        sys.exit(1)

    detach_igw(sys.argv[1], sys.argv[2])
