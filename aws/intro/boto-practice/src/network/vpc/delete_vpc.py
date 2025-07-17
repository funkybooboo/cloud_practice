#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client
from botocore.exceptions import ClientError


def delete_vpc(vpc_id: str) -> None:
    ec2: EC2Client = boto3.client("ec2")
    try:
        ec2.delete_vpc(VpcId=vpc_id)
        print(f"🗑️ Deleted VPC: {vpc_id}")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: delete_vpc.py <vpc-id>")
        sys.exit(1)

    delete_vpc(sys.argv[1])
