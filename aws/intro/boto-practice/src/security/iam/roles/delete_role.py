#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_iam.client import IAMClient


def delete_role(role_name: str) -> None:
    iam: IAMClient = boto3.client("iam")
    try:
        iam.delete_role(RoleName=role_name)
        print(f"🗑️ Deleted role: {role_name}")
    except ClientError as e:
        print(f"❌ Error deleting role {role_name}: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: delete_role.py <role-name>")
        sys.exit(1)
    delete_role(sys.argv[1])
