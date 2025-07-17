#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_iam.client import IAMClient


def delete_user(user_name: str) -> None:
    iam: IAMClient = boto3.client("iam")
    try:
        iam.delete_user(UserName=user_name)
        print(f"🗑️ Deleted user: {user_name}")
    except ClientError as e:
        print(f"❌ Error deleting user {user_name}: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: delete_user.py <user-name>")
        sys.exit(1)
    delete_user(sys.argv[1])
