#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_iam.client import IAMClient


def remove_user_from_group(user_name: str, group_name: str) -> None:
    iam: IAMClient = boto3.client("iam")
    try:
        iam.remove_user_from_group(GroupName=group_name, UserName=user_name)
        print(f"❌ Removed user '{user_name}' from group '{group_name}'")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: remove_user_from_group.py <user-name> <group-name>")
        sys.exit(1)
    remove_user_from_group(sys.argv[1], sys.argv[2])
