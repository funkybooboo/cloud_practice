#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_iam.client import IAMClient


def delete_group(group_name: str) -> None:
    iam: IAMClient = boto3.client("iam")
    try:
        iam.delete_group(GroupName=group_name)
        print(f"🗑️ Deleted group: {group_name}")
    except ClientError as e:
        print(f"❌ Error deleting group {group_name}: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: delete_group.py <group-name>")
        sys.exit(1)
    delete_group(sys.argv[1])
