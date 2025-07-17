#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client


def delete_igw(igw_id: str) -> None:
    ec2: EC2Client = boto3.client("ec2")
    ec2.delete_internet_gateway(InternetGatewayId=igw_id)
    print(f"🗑️ Deleted Internet Gateway: {igw_id}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: delete_internet_gateway.py <igw-id>")
        sys.exit(1)

    delete_igw(sys.argv[1])
