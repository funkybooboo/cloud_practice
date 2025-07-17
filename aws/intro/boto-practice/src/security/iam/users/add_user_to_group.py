#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_iam.client import IAMClient


def add_user_to_group(user_name: str, group_name: str) -> None:
    iam: IAMClient = boto3.client("iam")
    try:
        iam.add_user_to_group(GroupName=group_name, UserName=user_name)
        print(f"✅ Added user '{user_name}' to group '{group_name}'")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: add_user_to_group.py <user-name> <group-name>")
        sys.exit(1)
    add_user_to_group(sys.argv[1], sys.argv[2])
