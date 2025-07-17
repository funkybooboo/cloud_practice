#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client
from botocore.exceptions import ClientError


def delete_key_pair(name: str) -> None:
    ec2: EC2Client = boto3.client("ec2")
    try:
        ec2.delete_key_pair(KeyName=name)
        print(f"🗑️ Deleted key pair '{name}'")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: delete_key_pair.py <key-name>")
        sys.exit(1)
    delete_key_pair(sys.argv[1])
