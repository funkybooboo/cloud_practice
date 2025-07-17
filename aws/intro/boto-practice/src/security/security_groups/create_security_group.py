#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client
from botocore.exceptions import ClientError


def create_security_group(name: str, description: str, vpc_id: str) -> str:
    ec2: EC2Client = boto3.client("ec2")
    try:
        response = ec2.create_security_group(
            GroupName=name,
            Description=description,
            VpcId=vpc_id
        )
        group_id = response["GroupId"]
        print(f"✅ Created security group '{name}' with ID: {group_id}")
        return group_id
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: create_security_group.py <name> <description> <vpc-id>")
        sys.exit(1)
    create_security_group(sys.argv[1], sys.argv[2], sys.argv[3])
